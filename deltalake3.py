from pyspark.sql import SparkSession
from delta.tables import DeltaTable

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

print("Creating external Table object")
manual_path = "/home/rajneesh/deltalake/employees"
delta_table = DeltaTable.forPath(spark, manual_path)
delta_table.toDF().show()

print("Updating")
delta_table.update(condition="name = 'Bob'", set={"salary": "50000"})

print("Writing external table")
delta_df.write.mode("overwrite").option("overwriteSchema", "true").save(manual_path)

print("Reading external table")
delta_df = spark.read.load(manual_path)
delta_df.show()

# print("Appending bad data to Delta Lake")

# bad_df = spark.createDataFrame(
#    [(5, "Eve", "High")],
#    ["id", "name", "salary"]
# )

# bad_df.write.format("delta").mode("append").save(delta_path)
