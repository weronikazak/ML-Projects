import tensorflow as tf
import tensorflow.keras.layers as ly

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

print(x_train.shape)
print(x_train[0].shape)

model = tf.keras.models.Sequential()
model.add(ly.LSTM(128, input_shape=(x_train.shape[1:]), activation="relu", return_sequences=True))
model.add(ly.Dropout(0.2))

model.add(ly.LSTM(128, activation="relu"))
model.add(ly.Dropout(0.2))

model.add(ly.Dense(32, activation="relu"))
model.add(ly.Dropout(0.2))

model.add(ly.Dense(10, activation="softmax"))

model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam",
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=3, validation_data=(x_test, y_test))