from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF, IDF

conf = SparkConf().setMaster("local").setAppName("SparkTFIDF")
sc = SparkContext(conf=conf)

rawData = sc.textFile("data/subset-small.tsv")
fields = rawData.map(lambda x: x.split("\t"))
documents = fields.map(lambda x: x[3].split(" "))

documentNames = fields.map(lambda x: x[1])

hashingTF = HashingTF(100_000)
tf = hashingTF.transform(documents)

tf.cache()
idf = IDF(minDocFreq=2).fit(tf)
tfidf = idf.transform(tf)

word = ["Poland"]

wordTF = hashingTF.transform(word)
wordHashValue = int(wordTF.indices[0])

wordRelevance = tfidf.map(lambda x: x[wordHashValue])

zippedResults = wordRelevance.zip(documentNames)

print(f"Best document for the word {word[0]} is:")
print(zippedResults.max())