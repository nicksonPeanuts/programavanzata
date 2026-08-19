
from prog import VirtualVRAM
import numpy as np

byte = 0xAB

#print(bin(byte))
#print(byte >> 4)
#print(byte & 0x0F)


test = VirtualVRAM("../tiles.bin", "../sprites.bin")

print(len(test.bin_sprite))
print(set(test.bin_sprite))
print(np.unique(test.matrix_sprite))
print(np.count_nonzero(test.matrix_sprite))