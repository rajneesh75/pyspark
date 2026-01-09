from pyspark.sql.functions import *
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("test")
    .enableHiveSupport()
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", "./spark-warehouse")
    .config("spark.sql.hive.metastore.version", "2.3.10")
    .config("spark.sql.debug.maxToStringFields", "100")
    .config("spark.sql.hive.metastore.jars", "builtin")
    .getOrCreate()
)

print("Reading from Delta Lake")
bronze_df = spark.read.format("delta").table("events_bronze")
bronze_df.show()

valid_df = bronze_df.filter(
    col("event_id").isNotNull() &
    col("user_id").isNotNull() &
    (col("amount") > 0)
)
print("Valid Records:")
valid_df.show()

print("Invalid Records:")
invalid_df = bronze_df.subtract(valid_df)
invalid_df.show()

print("Writing Invalid Records:")
invalid_df.write.format("delta").mode("overwrite").saveAsTable("events_bad")

spark.sql("SELECT * FROM events_bad").show()

print("Calculating Data Quality Metrics:")
metrics = {
    "total_rows": bronze_df.count(),
    "valid_rows": valid_df.count(),
    "invalid_rows": invalid_df.count(),
}

metrics_df = spark.createDataFrame([metrics])
metrics_df.write.format("delta").mode("append").json("data_quality")
