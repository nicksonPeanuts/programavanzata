
from classi import VirtualVRAM
import numpy as np
import json


byte = 0xAB

#print(bin(byte))
#print(byte >> 4)
#print(byte & 0x0F)


test = VirtualVRAM("../tiles.bin", "../sprites.bin")

#print(len(test.bin_sprite))
#print(set(test.bin_sprite))
#print(np.unique(test.matrix_sprite))
#print(np.count_nonzero(test.matrix_sprite))


file = open("../scene.json", "r", encoding="utf-8")

data = json.load(file)
sprites = data["sprites"]

print(list(sprites[0]))