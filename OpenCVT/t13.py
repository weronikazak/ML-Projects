# morphological
import cv2
import numpy as np

# ------------
#   EROSION
# ------------
# usuwa granice obiektu na pierwszym planie.
# kernel przesuwa się po obrazie, pixel (1 lub 0) będzie uważany
# za 1 tylko wtedy, gdy wszystkie pixele pod jądrem mają wartosć 1,
# w przeciwnym razie ulegają erozji (są zerowane)
# w zależności od wielkości kernela pixele zostają odrzucone,
# biały obszar obrazu się zmniejsza

img = cv2.imread('images/j.png', 0)
# _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)

# -----------
#  DILATION
# -----------
# dylatacja - przeciwieństwo erozji

dilation = cv2.dilate(img, kernel, iterations=1)

# ----------
#  OPENING
# ----------
# erosion followed by dilation. użyteczna w usuwaniu szumu
# jakiekolwiek białe plamki na obrazie w tle zostają usunięte

img1 = cv2.imread('images/opening.png', 0)
opening = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel)


# ----------
#  CLOSING
# -----------
# przeciwieństwo openingu. Użyteczna w zapełnianiu 'dziur'

img2 = cv2.imread('images/closing.png', 0)
closing = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, kernel)


# ------------------------
# MORGPHOLOGICAL GRADIENT
# ------------------------
# a difference between dilation and erosion
# ma obraz ouline'u

gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)


# ----------
#  TOP HAT
# ----------
# różnica miedzy oryginalnym obrazem i openingiem

tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# ----------
# BLACK HAT
# ----------
# różnica między closingiem a oryginalnym obrazem

blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)


while True:
    cv2.imshow('img', img)
    cv2.imshow('erosion', erosion)
    cv2.imshow('dilation', dilation)
    cv2.imshow('opening', opening)
    cv2.imshow('closing', closing)
    cv2.imshow('gradient', gradient)
    cv2.imshow('tophat', tophat)
    cv2.imshow('blackhat', blackhat)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()