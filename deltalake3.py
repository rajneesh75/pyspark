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

print("Updating")
delta_table.update(condition="name = 'Bob'", set={"salary": "50000"})

print("Writing to Delta Lake")
delta_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(delta_path)

print("Reading from Delta Lake")
delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()

# print("Appending bad data to Delta Lake")

# bad_df = spark.createDataFrame(
#    [(5, "Eve", "High")],
#    ["id", "name", "salary"]
# )

# bad_df.write.format("delta").mode("append").save(delta_path)
