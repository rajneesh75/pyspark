from pyspark.sql.window import Window
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
    .getOrCreate()
)

bronze_df = (
    spark.read
    .option("multiline", "true")
    .json("./data/events1/events.json")
    .withColumn("ingestion_ts", current_timestamp())
)

bronze_df.show()

window = Window.partitionBy("event_id").orderBy(col("ingestion_ts").desc())
print(window)
