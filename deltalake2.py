from pyspark.sql import SparkSession



builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = builder.getOrCreate()


data = [
    (1, "Alice", 1000),
    (2, "Bob", 1500),
    (3, "Charlie", 2000)
]

df = spark.createDataFrame(data, ["id", "name", "salary"])
df.show()

delta_path = "/home/rajneesh/deltalake/employees"

print("Writing to Delta Lake")
df.write.format("delta").mode("overwrite").save(delta_path)


print("Reading from Delta Lake")
delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()
