import joblib
import time
import uuid
from pyspark.sql.functions import lit, struct, current_timestamp
from pyspark.sql.types import StringType
from pyspark.sql import SparkSession

builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = builder.getOrCreate()
print("Spark Session created")

model = joblib.load("churn_model.pkl")


MODEL_NAME = "customer_churn"
MODEL_VERSION = "v1.2.0"
MODEL_RUN_ID = "run_2026_01_07"

# Input data
input_df = spark.read.parquet("input_features")

start_time = time.time()
# Convert to Pandas for sklearn inference
pdf = input_df.toPandas()
pdf["prediction"] = model.predict(pdf)
pdf["score"] = model.predict_proba(pdf)[:, 1]

latency_ms = int((time.time() - start_time) * 1000)
# Back to Spark
pred_df = spark.createDataFrame(pdf)
