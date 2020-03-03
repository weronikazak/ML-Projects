import sklearn
import pickle
import pandas as pd
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier

pickle_in = open("student_grades.pickle", "rb")
linear1 = pickle.load(pickle_in)

pickle_in = open("studentgrades.pickle", "rb")
linear2 = pickle.load(pickle_in)

print(linear2)
print("------------------------")
print("Coefficient: ", linear2.coef_)
print("Intercept: ", linear2.intercept_)
print("------------------------")

