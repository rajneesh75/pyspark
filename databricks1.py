import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()
print("Loaded:", os.getenv("DATABRICKS_HOST"), os.getenv("DATABRICKS_TOKEN"), os.getenv("DATABRICKS_CLUSTER_ID"))

spark = (
    SparkSession.builder
    .remote(
        os.getenv("DATABRICKS_HOST"),
        os.getenv("DATABRICKS_TOKEN"),
        os.getenv("DATABRICKS_CLUSTER_ID")
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("INFO")
print(spark)
