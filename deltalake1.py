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

print("Spark Session created")
print(spark)


df = spark.createDataFrame(
    [(1, "A"), (2, "B")],
    ["id", "value"]
)

print("Writing to deltalake")
df.write.format("delta").mode("overwrite").saveAsTable("sample")


print("Reading from deltalake")
spark.read.table("sample").show()

print("Querying Delta Table as SQL Table")
spark.sql("""SELECT * FROM sample""").show()
