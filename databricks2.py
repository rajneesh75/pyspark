from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("INFO")
df = spark.read.csv("/Volumes/workspace/default/test/data_large.csv", header=True, inferSchema=True)
df_num = (df
          .withColumn("age", col("age").cast("int"))
          .withColumn("income", col("income").cast("double"))
          )

df_num.show(5)

city_indexer = StringIndexer(inputCol="city", outputCol="city_index")
city_indexed = city_indexer.fit(df_num).transform(df_num)
city_encoder = OneHotEncoder(inputCol="city_index", outputCol="city_vec")
city_encoded = city_encoder.fit(city_indexed).transform(city_indexed)

assembler = VectorAssembler(inputCols=["age", "income", "city_vec"], outputCol="features")
assembled_df = assembler.transform(city_encoded)
assembled_df.select("age", "income", "city", "city_vec", "features").show(5, truncate=False)

label_indexer = StringIndexer(inputCol="bought", outputCol="label",stringOrderType="alphabetAsc")

train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
lr = LogisticRegression(featuresCol="features", labelCol="label")
pipeline = Pipeline(stages=[city_indexer, city_encoder, assembler, label_indexer, lr])
model = pipeline.fit(train_df)
predictions_df = model.transform(test_df)
predictions_df.select("features", "label", "prediction", "probability").show(5)