import numpy as np

N = 5  # Number of rows
A = 0  # Starting value
B = 10  # Ending value

# Generate the row array with linearly increasing values
row = np.linspace(A, B, 6)

# Create the 2D array by repeating the row along the rows axis
arr = np.tile(row, (N, 1))

print(arr)