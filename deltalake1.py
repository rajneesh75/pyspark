from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("INFO")
print(spark)

df = spark.createDataFrame(
    [(1, "A"), (2, "B")],
    ["id", "value"]
)

df.write.format("delta").mode("overwrite").save("/tmp/delta-table")
spark.read.format("delta").load("/tmp/delta-table").show()