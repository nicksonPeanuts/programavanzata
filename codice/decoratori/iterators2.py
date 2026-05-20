from itertools import product, chain, pairwise, permutations, combinations, repeat

a = [1, 2, 3, 4]
b = [5, 6, 7, 8]
c = [9, 10, 11, 12, 13, 14, 15]

print("Concatenazione di iteratori")
for i in chain(a, b, c):
    print(i)

# implementazione di chain
def mychain(*iters):
    # per ogni iteratore negli iterabile
    for i in iters:
        # per ogni elemento nell'iterabile
        for e in i:
            # prendimi quello
            yield e

mychain(a,b)
for i in mychain(a,b):
    print(i)

print("Prodotto di iteratori")
for i, j in product(a, b):
    print(f"{i}, {j}")


print("Myproduct")
def myproduct(a, b):
    for i in a:
        for j in b:
            yield (i,j)

for i in myproduct(a,b):
    print(i)

print("Iterazione sulle coppie di valori")
for i, j in pairwise(a):
    print(f"{i}, {j}")

def mypairwise(a,b):
    return NotImplementedError

print("Iterazione sulle permutazioni")
for i in permutations(a):
    print(i)

print("Iterazione sulle combinazioni")
for i in combinations(a, r=2):
    print(i)

print("Ripetizione di uno stesso valore")
for i in repeat("ciao", 10):
    print(i)


def myrepeat(x, n=-1):
    i = 0
    while i != n:
        i += 1
        yield x