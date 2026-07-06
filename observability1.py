from pyspark.sql.functions import *
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("test")
    .enableHiveSupport()
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", "./spark-warehouse")
    .config("spark.sql.hive.metastore.version", "2.3.10")
    .config("spark.sql.debug.maxToStringFields", "100")
    .config("spark.sql.hive.metastore.jars", "builtin")
    .getOrCreate()
)