# canny edge detection
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/img.jpg', 0)
edges = cv2.Canny(img, 100, 200)

plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(edges, cmap='gray')
plt.title('Edge Image')
plt.xticks([])
plt.yticks([])

plt.show()

# Canny edge detector: po kolei
# 1. redukuje hałas za pomocą filtru Gaussa
# 2. wygyładzony obraz jest potem filtowany za pomocą sobela pionowo i poziomo
# 3. potem za pomocą danych znajduje się gradient i kierunek krawędzi dla każdego pixela
# 4. po uzyskaniu wielkości i kierunku gradientu, wykonywane jest skanowanie obrazu w celu usuniecia
# niepożądanych pixeli, które mogą nie stanowić krawędzi
# 5. thresholdingowanie