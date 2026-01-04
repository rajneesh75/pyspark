from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()


print("Reading from deltalake")
delta_path = "/tmp/delta/employees"
delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()


new_df = spark.createDataFrame(
    [(6, "Frank", 3000, "IT")],
    ["id", "name", "salary", "dept"]
)

print("Writing to deltalake")
new_df.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(delta_path)

print("Reading from deltalake")
delta_path = "/tmp/delta/employees"
delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()