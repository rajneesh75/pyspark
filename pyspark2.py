from pyspark.sql import SparkSession

builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = builder.getOrCreate()

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data_large.csv")
    .select("age", "income", "city")
)

df.show()
print("Writing input features to Parquet")
df.write.mode("overwrite").parquet(
    "/home/rajneesh/Python/pyspark/input_features"
)
