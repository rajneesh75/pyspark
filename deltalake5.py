from pyspark.sql import SparkSession
from delta.tables import DeltaTable

builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = builder.getOrCreate()
delta_path = "/home/rajneesh/deltalake/employees"


print("Reading from deltalake")

delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()

print("Creating Delta Table object")
delta_table = DeltaTable.forPath(spark, delta_path)
delta_table.toDF().show()

print("Registering Delta Table as SQL Temporary View")
delta_df.createOrReplaceTempView("people")
spark.sql("""SELECT * FROM people""").show()

print("Saving Delta Table as SQL Table")
delta_df.write.mode("overwrite").saveAsTable("employees")

print("Querying Delta Table as SQL Table")
spark.sql("""SELECT * FROM employees""").show()
