# image gradients
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/photo.jpg', 0)

laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

plt.subplot(2, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.xticks([])
plt.yticks([])

# LAPLACIAN
# wylicza laplaciana obrazu. Coś z pochodnymi i sobelami

plt.subplot(2, 2, 2)
plt.imshow(laplacian, cmap='gray')
plt.title('Laplacian')
plt.xticks([])
plt.yticks([])

# SOBEL
# operacja wygładzania Gaussa i różnicowania, bardziej odporna na hałas

plt.subplot(2, 2, 3)
plt.imshow(sobelx, cmap='gray')
plt.title('SobelX')
plt.xticks([])
plt.yticks([])

plt.subplot(2, 2, 4)
plt.imshow(sobely, cmap='gray')
plt.title('SobelY')
plt.xticks([])
plt.yticks([])

plt.show()

# datatype w w/w przykładach - CV_8V albo np.uint8 
# black to white transition przyjmuje się jako nachylenie pozytywne
# w drugą strone jest jednak negatywne. Wartości negatywne podczas konwersji na uint8
# są zerowane. "Przewaga" jest tracona
# dlatego lepiej utrzymywać wartość w wyższych postaciach, typu
# cv2.CV_16S, cv2.CV_64F, a potem przekonwertować na cv2.CV_8U

sobelx8u = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=5)

# take the 8U type and convert it to 64f, then take its absolute ans convert back to 8u
sobelx64f = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
abs_sobelx64f = np.absolute(sobelx64f)
sobel_8u = np.uint8(abs_sobelx64f)

plt.subplot(1,3,1)
plt.imshow(img,cmap = 'gray')
plt.title('Original')
plt.xticks([])
plt.yticks([])

plt.subplot(1,3,2)
plt.imshow(sobelx8u,cmap = 'gray')
plt.title('Sobel CV_8U')
plt.xticks([])
plt.yticks([])

plt.subplot(1,3,3)
plt.imshow(sobel_8u,cmap = 'gray')
plt.title('Sobel abs(CV_64F)')
plt.xticks([])
plt.yticks([])

plt.show()