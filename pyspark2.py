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

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data_large.csv")
    .select("age", "income", "city")
)

df.show()
print("Writing input features as Parquet managed table")
df.write.format("delta").mode("overwrite").saveAsTable("input_features", format("parquet"))
