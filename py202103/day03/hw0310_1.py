# stride = 2 步长 window = 4
import numpy as np

array = np.arange(1,15,1)
start = 0
stride = 2
window = 4
data = []
while start < (len(array)-window):
    data.append(array[start:start+window])
    start += stride
    pass
print(np.array(data))

