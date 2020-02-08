# CONTOURS HIERARCHY
import cv2
import numpy as np

# szukanie konturów zaczyna się od TOP i idzie w dół
# w przypadku pudełowatych koturnów najpierw znajduje
# linię najbliżej TOPU, potem pudełkowaty obwód jako całość

# [ NEXT, PREVIOUS, FIRST_CHILD, PARENT ]
# NEXT oznacza następny kontur na tym samym poziomie hierarchicznym
# PREVIOUS oznancza poprzedni kontur (..)
# FIRST_CHILD oznacza jego pierwsze dziecko (dla 2 to 2a, dla 2a 3)
# PARENT znacza index konturu rodzica (dla 3 i 2a to 2)
# /// jeśli kontur nie posiada rodzica, PARENT zwraca -1


# ----------------------
# CONTOUR RETRIEVAL MODE
# ----------------------

# 1. RETR_LIST
# PARENTS i CHILDREN są równi i wszystkie należą do tego samego poziomu hierarchii
# dobry, jeśli nie chce się żadnych hierarchical zasad

# 2. RETR_EXTERNAL
# tylko najstarszy PARENT jest istotny, reszta nie za bardzo

# 3. RETR_CCOMP
# liczy od środka po kolei

# 4. RETR_TREE
# nie tylko pokazuje relacje PARENT-CHILD ale także wczesniejsze/późniejsze(grandpa, father, son, grandson...)

