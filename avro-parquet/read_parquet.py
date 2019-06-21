from pyspark import SparkContext
from pyspark.sql import SQLContext
sc = SparkContext()
sqlContext = SQLContext(sc)
df = sqlContext.read.parquet('sample.parquet')

print(df)

