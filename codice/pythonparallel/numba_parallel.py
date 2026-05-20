from numba import jit, prange
import timeit
import numpy as np

def f_n(v1, v2):
    res = 0.0
    for i in range(len(v1)):
        res += v1[i] * v2[i]
    return res

@jit
def g_n(v1, v2):
    res = 0.0
    for i in range(len(v1)):
        res += v1[i] * v2[i]
    return res

@jit(parallel=True)
def h_n(v1, v2):
    res = 0.0
    for i in prange(len(v1)):
        res += v1[i] * v2[i]
    return res

n = 100_000_000
v1 = np.random.rand(n)
v2 = np.random.rand(n)
vout = np.zeros(n)
print(f"Esecuzione di f_n: {timeit.timeit(lambda: f_n(v1, v2), number=1)}")
print(f"Esecuzione di g_n: {timeit.timeit(lambda: g_n(v1, v2), number=1)}")
print(f"Esecuzione di h_n: {timeit.timeit(lambda: h_n(v1, v2), number=1)}")