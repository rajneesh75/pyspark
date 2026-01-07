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

print("Reading from deltalake")
delta_df = spark.read.format("delta").table("employees")
delta_df.show()

new_df = spark.createDataFrame(
    [(6, "Frank", 10000, "IT")],
    ["id", "name", "salary", "dept"]
)

print("Writing to deltalake")
new_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .saveAsTable("employees")

print("Reading from deltalake")
delta_df = spark.read.format("delta").table("employees")
delta_df.show()
