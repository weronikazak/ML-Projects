from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors

spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("LinearRegression").getOrCreate()

inputLines = spark.sparkContext.textFile("data/regression.txt")
data = inputLines.map(lambda x: x.split(",")).map(
	lambda x: (float(x[0]), Vectors.dense(float(x[1]))))

colnames = ["label", "features"]
df = data.toDF(colnames)

trainTest = df.randomSplit([0.5, 0.5])
trainingDF = trainTest[0]
testDF = trainTest[1]

lir = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

model = lir.fit(trainingDF)

fullPrediction = model.transform(testDF).cache()

predictions = fullPrediction.select("prediction").rdd.map(lambda x: x[0])
labels = fullPrediction.select("label").rdd.map(lambda x: x[0])

predictionAndLabel = predictions.zip(labels).collect()

for prediction in predictionAndLabel:
	print(prediction)

spark.stop()