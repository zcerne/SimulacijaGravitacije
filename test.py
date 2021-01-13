import numpy as np
import matplotlib.pyplot as plt

a = []
for i in range(10):
    a.append([i, i+1])
a = np.array(a)
print(a)