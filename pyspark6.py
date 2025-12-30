from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType


def square(x):
    return x * x


square_udf = udf(square, IntegerType())

spark = SparkSession.builder \
    .appName("Test") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("INFO")

teachers = [
    (1, "Raj", 35, 1),
    (2, "Amit", 30, 2),
    (3, "Neha", 28, 1),
    (4, "test", 34, 1)
]
teachers_columns = ["id", "teacher_name", "age", "subject_code"]

print("Creating dataframe")
dfteachers = spark.createDataFrame(teachers, teachers_columns)
dfteachers.show()

print("Caching")
dfteachers.cache()
dfteachers.persist()

print("Adding column")
dfteachers.withColumn("age_squared", square_udf(dfteachers.age)).show()
dfteachers.write.mode("overwrite").parquet("output/")

dfteachers.write.csv("output/csv")
dfteachers.write.json("output/json")
