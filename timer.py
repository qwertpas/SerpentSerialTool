import timeit
import numpy as np


def function_1():
    scaled_data = np.random.random((3, 5))

    labellen, historylen = scaled_data.shape

    xvals_row = np.linspace(start=0, stop=historylen, num=historylen)
    xvals_arr = np.tile(xvals_row, (labellen, 1))

    both = np.dstack([xvals_arr, scaled_data]).reshape(labellen,historylen*2)
    print(both)
    return both

def function_2():
    xvals = np.linspace(start=0, stop=100, num=100)
    return xvals




np.set_printoptions(precision=2, suppress=True)

function_1()

# Measure the execution time of function_1
# time_1 = timeit.timeit(function_1, number=100)

# Measure the execution time of function_2
# time_2 = timeit.timeit(function_2, number=100)

# print("Execution time of function 1:", time_1)
# print("Execution time of function 2:", time_2)