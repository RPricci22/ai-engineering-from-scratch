import numpy as np

A = np.array([[3, 4], [5, 6]])
B = 5

C = A + B
print(C)


# Array A: Shape (3, 4)
# 3 rows, 4 columns
D = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

# Array B: Shape (4,)
# A 1-dimensional array with 4 elements
E = np.array([10, 20, 30, 40])

F = D + E
print(F)
