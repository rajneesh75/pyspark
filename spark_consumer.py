from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, LongType


spark = SparkSession.builder \
    .appName("KafkaConsumer") \
    .getOrCreate()

spark.sparkContext.setLogLevel("INFO")

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user_events") \
    .option("startingOffsets", "latest") \
    .load()


# Schema
schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("age", IntegerType()),
    StructField("income", IntegerType()),
    StructField("city", StringType()),
    StructField("timestamp", LongType())
])

# Parse JSON
parsed_df = kafka_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Write stream (THIS IS REQUIRED)
query = parsed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
