from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()


data = [
    (1, "Alice", 1000),
    (2, "Bob", 1500),
    (3, "Charlie", 2000)
]

df = spark.createDataFrame(data, ["id", "name", "salary"])
df.show()

delta_path = "/home/rajneesh/deltalake/employees"
df.write.format("delta").mode("overwrite").save(delta_path)

print("Appending bad data to Delta Lake")

delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()
