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

print(spark)

spark.sql("SET spark.sql.warehouse.dir").show(truncate=False)
