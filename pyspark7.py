from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("test")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", "./spark-warehouse")
    .config("spark.sql.cli.print.header", "true")
    .config("spark.sql.cli.pretty", "true")
    .getOrCreate()
)

data = [
    (1, "Raj", 35),
    (2, "Amit", 30),
    (3, "Neha", 28)
]

columns = ["id", "name", "age"]

df = spark.createDataFrame(data, columns)
df.show()
df.printSchema()
