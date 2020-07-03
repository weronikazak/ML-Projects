import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras.layers as ly
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import ResNet50
from sklearn.metrics import classification_report
from tensorflow.keras.models import Model
from imutils import paths


TRAIN_PATH = "camouflage_images/training"
VAL_PATH = "camouflage_images/validation"
TEST_PATH = "camouflage_images/testing"


train_aug = ImageDataGenerator(
    rotation_range=25,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)

val_aug = ImageDataGenerator()

mean = np.array([123.68, 116.779, 103.939], dtype="float32")
train_aug.mean = mean
val_aug.mean = mean


train_gen = train_aug.flow_from_directory(
    TRAIN_PATH,
    class_mode="categorical",
    target_size=(224, 224),
    color_mode="rgb",
    shuffle=True,
    batch_size=32
)

val_gen = val_aug.flow_from_directory(
    VAL_PATH,
    target_size="categorical",
    class_mode="categorical",
    target_size=(224, 224),
    color_mode="rgb",
    shuffle=True,
    batch_size=32
)

test_gen = val_aug.flow_from_directory(
    TEST_PATH,
    class_mode="categorical",
    target_size=(224, 224),
    color_mode="rgb",
    shuffle=True,
    batch_size=32
)


baseModel = ResNet50(weights="imagenet", include_top=False, input_tensor=ly.Input(shape=(224, 224, 3)))

m = baseModel.output
m = ly.AveragePooling2D(pool_size=(7, 7))(m)
m = ly.Flatten()(m)
m = ly.Dense(256, activation="relu")(m)
m = ly.Dropout(0.5)(m)
m = ly.Dense(2, activation="softmax")(m)

model = Model(inputs=baseModel.input, outputs=m)

for layer in baseModel.layers:
    layer.trainable = False

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit_generator(
    train_gen,
    steps_per_epoch=len(list(paths.list_images())) // 32,
    validation_data=val_gen,
    validation_steps=len(list(paths.list_images)) // 32,
    epochs=20
)

test_gen.reset()
model.save("data/camouflage.model")

