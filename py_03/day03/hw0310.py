import numpy as np
def gen_strides(a, stride_len=5, window_len=5):
    n_strides = ((a.size - window_len) // stride_len) + 1
    return np.array([a[s:(s + window_len)] for s in np.arange(0, n_strides * stride_len, stride_len)])
print(gen_strides(np.arange(15), stride_len=2, window_len=4))
