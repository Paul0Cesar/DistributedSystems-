from pyspark.sql import SparkSession

scala_version = '2.12'
spark_version = '3.2.2'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.1'
]

def new_element(element):
    print(element)

topic="BTC_CURRENCY"
spark = SparkSession \
            .builder \
            .appName("BTC_CURRENCY_APP") \
            .config("spark.jars.packages", ",".join(packages))\
            .getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "BTC_CURRENCY") \
  .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


ds = df \
  .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
  .writeStream \
  .format("kafka") \
  .option("checkpointLocation", "./tmp") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "BTC_CURRENCY") \
  .foreach(new_element)\
  .start()

ds.awaitTermination()