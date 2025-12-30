from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("INFO")

data = [
    (1, "Raj", 35),
    (2, "Amit", 30),
    (3, "Neha", 28)
]

columns = ["id", "name", "age"]

df = spark.createDataFrame(data, columns)
#df.explain(True)
df.show()
df.printSchema()
