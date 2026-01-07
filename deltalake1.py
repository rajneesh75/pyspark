from pyspark.sql import SparkSession


builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = builder.getOrCreate()

print(spark)
delta_path = "/home/rajneesh/deltalake/sample"

df = spark.createDataFrame(
    [(1, "A"), (2, "B")],
    ["id", "value"]
)

print("Writing to deltalake")
df.write.format("delta").mode("overwrite").save(delta_path)

print("Reading from deltalake")
spark.read.format("delta").load(delta_path).show()