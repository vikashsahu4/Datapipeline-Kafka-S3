import json
from io import BytesIO
import fastavro
from pyspark import SparkContext
from pyspark.sql import SQLContext
sc = SparkContext()
sqlContext = SQLContext(sc)
'''
from pyspark import SparkContext
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
sc = SparkContext()
sqlContext = SQLContext(sc)
#df = spark.read.format("avro").load("sample.avro")
df = sqlContext.read.format("com.databricks.spark.avro").load("sample.avro")
df.show()
sc.stop()
'''

with open('data_schema.json') as f:
    schema = json.load(f)

print(type(schema))
print(schema)

rdd = sc.binaryFiles("/home/vsahu/project/spark/sample.avro").flatMap(lambda args: fastavro.reader(BytesIO(args[1]), reader_schema=schema))
print(rdd.collect())

df=rdd.toDF()
#df = sqlContext.createDataFrame(rdd, schema)

df.write.parquet("sample1.parquet")

