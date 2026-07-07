from pyspark.sql import SparkSession
from delta.tables import DeltaTable



spark = (
    SparkSession.builder
    .appName("test")
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

print(spark.version)
print("Reading from Delta Lake")

delta_df = (
    spark.read
    .format("delta")
    .load("./spark-warehouse/employees")
)

delta_df.show()
manual_path = "/home/rajneesh/external_tables/employees"
print("Writing external Delta table")

delta_df.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .format("delta") \
    .save(manual_path)

print("Creating DeltaTable object")

delta_table = DeltaTable.forPath(
    spark,
    manual_path
)

delta_table.toDF().show()

print("Updating")

delta_table.update(
    condition="name = 'Bob'",
    set={
        "salary": "50000"
    }
)

print("After update")

delta_table.toDF().show()
