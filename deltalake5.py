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

print("Reading from deltalake")

delta_df = spark.read.format("delta").table("employees")
delta_df.show()

print("Registering Delta Table as SQL Temporary View")
delta_df.createOrReplaceTempView("people")
spark.sql("""SELECT * FROM people""").show()

print("Saving Delta Table as SQL Table")
delta_df.write.mode("overwrite").saveAsTable("people")

print("Querying Delta Table as SQL Table")
spark.sql("""SELECT * FROM people""").show()
