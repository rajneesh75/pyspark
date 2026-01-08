from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("test")
    .enableHiveSupport()
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", "./spark-warehouse")
    .config("spark.sql.cli.print.header", "true")
    .config("spark.sql.cli.pretty", "true")
    .config(
        "spark.sql.streaming.stateStore.providerClass",
        "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider")
    .getOrCreate()
)

schema = "user_id INT, event STRING, ts TIMESTAMP"
print("Reading streaming data from ./data/events")

spark.readStream \
    .format("json") \
    .schema(schema) \
    .load("./data/events") \
    .writeStream \
    .format("delta") \
    .option("checkpointLocation", "./chk/events") \
    .toTable("events_bronze")\
    .awaitTermination()

