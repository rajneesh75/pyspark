import time
import joblib
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    lit,
    current_timestamp,
    struct,
    expr
)
from pyspark.sql.types import StringType

spark = (
    SparkSession.builder
    .appName("OSS-Inference-Table")
    .enableHiveSupport()
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", "/home/rajneesh/Python/pyspark/spark-warehouse")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")
print("Spark Session created")

# Enable schema evolution
spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")

# -------------------------------------------------------------------
# 2. Load Model
# -------------------------------------------------------------------

model = joblib.load("churn_model.pkl")

MODEL_NAME = "customer_churn"
MODEL_VERSION = "v1.2.0"
MODEL_RUN_ID = "run_2026_01_07"

FEATURE_COLS = ["age", "income", "city"]

# -------------------------------------------------------------------
# 3. Read Input Features
# -------------------------------------------------------------------

input_df = spark.read.parquet("input_features")

features_df = input_df.select(*FEATURE_COLS)

# -------------------------------------------------------------------
# 4. Inference (SAFE sklearn usage)
# -------------------------------------------------------------------

start_time = time.time()
pdf = features_df.toPandas()

# 🔑 NEVER mutate input features
X = pdf[FEATURE_COLS].copy()

pdf["prediction"] = model.predict(X)
pdf["score"] = model.predict_proba(X)[:, 1]

latency_ms = int((time.time() - start_time) * 1000)

pred_df = spark.createDataFrame(pdf)

# -------------------------------------------------------------------
# 5. Build Inference Table Schema
# -------------------------------------------------------------------

print("Building inference DataFrame")
inference_df = (
    pred_df
    .withColumn("inference_id", expr("uuid()"))
    .withColumn("event_time", current_timestamp())
    .withColumn("model_name", lit(MODEL_NAME))
    .withColumn("model_version", lit(MODEL_VERSION))
    .withColumn("model_run_id", lit(MODEL_RUN_ID))
    .withColumn(
        "inputs",
        struct(*FEATURE_COLS)
    )
    .withColumn(
        "predictions",
        struct("prediction", "score")
    )
    .withColumn("latency_ms", lit(latency_ms))
    .withColumn("status", lit("SUCCESS"))
    .withColumn("error_message", lit(None).cast(StringType()))
)

print("Writing inference data to Delta table")

spark.sql("CREATE SCHEMA IF NOT EXISTS ml_prod")
inference_df.write.format("delta").mode("append").saveAsTable(
    "ml_prod.inference_customer_churn"
)

print("Inference data written to Delta table")


spark.sql("""
    SELECT inference_id, model_version, predictions.score, event_time
    FROM ml_prod.inference_customer_churn
    ORDER BY event_time DESC
    LIMIT 5
""").show(truncate=False)
