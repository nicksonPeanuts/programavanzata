from numba import vectorize, guvectorize, jit, float64
import numpy as np
import timeit

def standard_fma(va, vb, vc):
    out = np.empty_like(va)
    for i in range(va.shape[0]):
        out[i] = va[i] * vb[i] + vc[i]
    return out

@jit
def jit_fma(va, vb, vc):
    out = np.empty_like(va)
    for i in range(va.shape[0]):
        out[i] = va[i] * vb[i] + vc[i]
    return out

@vectorize([float64(float64, float64, float64)], target='cpu')
def vectorized_fma(a, b, c):
    return a * b + c

@guvectorize([(float64[:], float64[:], float64[:], float64[:])],
             '(n),(n),(n)->(n)')
def guvectorized_fma(a, b, c, out):
    for i in range(a.shape[0]):
        out[i] = a[i] * b[i] + c[i]

@guvectorize([(float64[:], float64[:], float64, float64[:])],
             '(n),(n),()->(n)')
def guvectorized_fma_fixed_c(a, b, c, out):
    for i in range(a.shape[0]):
        out[i] = a[i] * b[i] + c

n = 1_000_000
rng = np.random.default_rng()
a = rng.random(n)
b = rng.random(n)
c = rng.random(n)
out = np.empty_like(a)


print(f"Esecuzione di standard_fma: {timeit.timeit(lambda: standard_fma(a, b, c), number=1)}")
print(f"Esecuzione di jit_fma: {timeit.timeit(lambda: jit_fma(a, b, c), number=1)}")
print(f"Esecuzione di vectorized_fma: {timeit.timeit(
    lambda: vectorized_fma(a, b, c), number=1)}")
guvectorized_fma(a, b, c, out)
print(f"Esecuzione di guvectorized_fma: {timeit.timeit(
    lambda: guvectorized_fma(a, b, c, out), number=1)}")

print(f"Esecuzione di guvectorized_fma with fixed c: {timeit.timeit(
    lambda: guvectorized_fma_fixed_c(a, b, 0.5, out), number=1)}")