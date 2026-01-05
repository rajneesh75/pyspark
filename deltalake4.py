from pyspark.sql import SparkSession


builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = builder.getOrCreate()
delta_path = "/home/rajneesh/deltalake/employees"
print("Reading from deltalake")
delta_df = spark.read.format("delta").load(delta_path)
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
    .save(delta_path)

print("Reading from deltalake")
delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()