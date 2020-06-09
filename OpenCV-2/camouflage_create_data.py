import os
import cv2
import numpy as np
import random
from imutils import paths

random.seed(42)

CLASSES = ["camouflage_clothes", "normal_clothes"]

VAL_SPLIT = 0.1
TRAIN_SPLIT = 0.75

f

i = int(TRAIN_SPLIT)

BATCH_SIZE = 32
EPOCHS = 20


random.shuffle
