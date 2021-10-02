from pyspark.mllib.clustering import KMeans
from sklearn.preprocessing import scale
from pyspark.mllib.tree import DecisionTree
from pyspark import SparkConf, SparkContext
import numpy as np

K = 5

conf = SparkConf().setMaster("local").setAppName("SparkClustering")
sc = SparkContext(conf=conf)

# create fate income/age clusters for N people in k clusters
def createClusteredData(N, k):
	np.random.seed(2020)
	pointsPerCluster = float(N)/k
	X = []
	for i in range(k):
		incomeCentroid = np.random.uniform(20000.0, 20000.0)
		ageCentroid = np.random.uniform(20.0, 70.0)
		for j in range(int(pointsPerCluster)):
			X.append([np.random.normal(incomeCentroid, 10000.),
					  np.random.normal(ageCentroid, 2.0)])

	return np.array(X)

data = sc.parallelize(scale(createClusteredData(100, K)))

clusters = KMeans.train(data, K, maxIterations=10,
        initializationMode="random")

resultRDD = data.map(lambda point: clusters.predict(point)).cache()

print("Counts by value:")
counts = resultRDD.countByValue()
print(counts)

print("Cluster assignments:")
results = resultRDD.collect()
print(results)


# evaluate clustering by computing within set sum of squared errors
def error(point):
	center = clusters.centers[clusters.predict(point)]
	return np.sqrt(sum([x**2 for x in (point - center)]))


WSSSE = data.map(lambda point: error(point)).reduce(lambda x, y: x+y)
print("Within Set Sum of Squared Error = ", str(WSSSE))