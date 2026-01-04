from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable

builder = (
    SparkSession.builder
    .appName("DeltaSpark4")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()


print("Reading from deltalake")
delta_path = "/tmp/delta/employees"
delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()

delta_table = DeltaTable.forPath(spark, delta_path)


print("Updating")
delta_table.update(
    condition="name = 'Bob'",
    set={"salary": "50000"}
)


delta_df = delta_table.toDF()
delta_df.show()

print("Writing to Delta Lake")
delta_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(delta_path)

print("Reading from Delta Lake")
delta_df = spark.read.format("delta").load(delta_path)
delta_df.show()

print("Appending bad data to Delta Lake")

bad_df = spark.createDataFrame(
    [(5, "Eve", "High")],
    ["id", "name", "salary"]
)

bad_df.write.format("delta").mode("append").save(delta_path)
