from pyspark.sql import SparkSession

builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config(
        "spark.jars.packages",
        "io.delta:delta-spark_2.13:3.0.0"
    )
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
)

spark = builder.getOrCreate()
print(spark)
