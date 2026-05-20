from numba import jit, prange
import timeit
import numpy as np

def matmul(M1, M2):
    Mout = np.zeros_like(M1)
    for i in range(M1.shape[0]):
        for j in range(M1.shape[1]):
            s = 0.0
            for k in range(M1.shape[1]):
                Mout[i, j] += M1[i, k] * M2[k, j]
    return Mout

@jit
def matmul_jit(M1, M2):
    Mout = np.zeros_like(M1)
    for i in range(M1.shape[0]):
        for j in range(M1.shape[1]):
            for k in range(M1.shape[1]):
                Mout[i, j] += M1[i, k] * M2[k, j]
    return Mout

@jit(parallel=True)
def matmul_parallel(M1, M2):
    Mout = np.zeros_like(M1)
    for i in prange(M1.shape[0]):
        for j in prange(M1.shape[1]):
            for k in range(M1.shape[1]):
                Mout[i, j] += M1[i, k] * M2[k, j]
    return Mout

n = 250
M1 = np.random.rand(n, n)
M2 = np.random.rand(n, n)
print(f"Esecuzione di matmul: {timeit.timeit(lambda: matmul(M1, M2), number=1)}")
print(f"Esecuzione di matmul_jit: {timeit.timeit(lambda: matmul_jit(M1, M2), number=1)}")
print(f"Esecuzione di matmul_parallel: {timeit.timeit(lambda: matmul_parallel(M1, M2), number=1)}")