from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark import SparkConf, SparkContext
import numpy as np

conf = SparkConf().setMaster("local").setAppName("SparkDecisionTree")
sc = SparkContext(conf=conf)

# convert "yes" to 1 and "no" to 0
def changeYesNo(YN):
	if YN == "Y":
		return 1
	else:
		return 0

def mapEducation(degree):
	if degree == "BS":
		return 1
	elif degree == "MS":
		return 2
	elif degree == "PhD":
		return 3
	else:
		return 0

def createLabeledPoints(fields):
	yearsExperience = int(fields[0])
	employed = changeYesNo(fields[1])
	previousEmployers = int(fields[2])
	educationLevel = mapEducation(fields[3])
	topTier = changeYesNo(fields[4])
	interned = changeYesNo(fields[5])
	hired = changeYesNo(fields[6])

	return LabeledPoint(hired, np.array([yearsExperience, employed, previousEmployers,
						educationLevel, topTier, interned]))

rawData = sc.textFile("data/pastHires.csv")
header = rawData.first()
rawData = rawData.filter(lambda x: x!= header)

csvData = rawData.map(lambda x: x.split(","))

trainingData = csvData.map(createLabeledPoints)

testCandidates = [np.array([10, 1, 3, 1, 0, 0])]
testData = sc.parallelize(testCandidates)

model = DecisionTree.trainClassifier(trainingData,
									numClasses=2,
									categoricalFeaturesInfo={1:2, 3:4, 4:2, 5:2},
									impurity="gini",
									maxDepth=5,
									maxBins=32)

predictions = model.predict(testData)
results = predictions.collect()

print("Hire prediction:")
for r in results:
	print(r)

print("Learned classification tree model:")
print(model.toDebugString())
