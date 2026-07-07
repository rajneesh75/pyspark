from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("test")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", "./spark-warehouse")
    .getOrCreate()
)

data = [
    (1, "Alice", 1000),
    (2, "Bob", 1500),
    (3, "Charlie", 2000)
]

df = spark.createDataFrame(data, ["id", "name", "salary"])
df.show()

print("Writing to Delta Lake")
df.write.format("delta").mode("overwrite").saveAsTable("employees")

print("Reading from Delta Lake")
delta_df = (
    spark.read
    .format("delta")
    .load("./spark-warehouse/employees")
)

delta_df.show()
