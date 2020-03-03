import sklearn
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import linear_model
import pickle
import matplotlib.pyplot as plt

data = pd.read_csv('student_mat.csv', sep=";")

data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]
data= shuffle(data)
# print(data.head())

predict = "G3"

X = np.array(data.drop([predict], 1))
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

# linear = linear_model.LinearRegression()
# linear.fit(x_train, y_train)
# acc = linear.score(x_test, y_test)
#
# print(acc)
# print("Coefficient: ", linear.coef_) # współczynnik - wartość każdego nachylenia
# print("Intercepr:", linear.intercept_) # przechwyt
#
# predictions = linear.predict(x_test) # a list of all predicitons
# for i in range(len(predictions)):
#     print(predictions[i], x_test[i], y_test[i])
#
# with open("student_grades.pickle", "wb") as f:
#     pickle.dump(linear, f)

best = 0
for i in range(20):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    acc = linear.score(x_test, y_test)
    print("Accuracy: ", str(acc))

    if acc > best:
        best = acc
        with open("studentgrades.pickle", "wb") as f:
            pickle.dump(linear, f)


prediction = linear.predict(x_test)
for i in range(len(prediction)):
    print(prediction[i], x_test[i], y_test[i])

plot = "failures"
plt.scatter(data[plot], data['G3'])
plt.legend(loc=4)
plt.xlabel("failures")
plt.ylabel("Final grade")
plt.show()