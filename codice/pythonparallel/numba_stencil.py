import numpy as np
from numba import jit, stencil
from matplotlib import pyplot as plt
from matplotlib import animation

n = 200
arr = np.zeros((n, n))

arr[n//2:n//2+10, n//2:n//2+10] = 1.0
arr[n//3:n//3+20, n//3:n//3+20] = 1.0
arr[n//4:n//4+10, n//4:n//4+10] = 1.0

@stencil(neighborhood=((-1, 1), (-1, 1)))
def stencil_2d(arr):
    s = 0.0
    for i in range(-1, 2):
        for j in range(-1, 2):
            s += arr[i, j]
    return s / 9.0

@jit(parallel=True)
def apply_stencil(arr):
    result = np.zeros_like(arr)
    stencil_2d(arr, out=result)
    return result

fig, ax = plt.subplots()
im = ax.imshow(arr, cmap='grey')
ax.axis('off')

def update(frame):
    global arr
    arr = apply_stencil(arr)
    im.set_data(arr)
    return (im,)

ani = animation.FuncAnimation(fig, update, frames=1000, interval=50, blit=False)
plt.show()