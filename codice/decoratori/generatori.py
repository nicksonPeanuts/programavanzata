def simple_gen():
    yield 1
    yield 2
    yield 3


x = simple_gen()
print(next(x))
print(next(x))
print(next(x))


def squares(n_elems):
    for n in range(n_elems):
        yield n**2

def cubes(num_cubes):
    for n in range(num_cubes):
        yield n**3

# generatore per caricare dataset in memoria senza portare dentro troppi MB
def data_loader(data_):
    for line in data_:
        yield line


s = squares(10)
c = cubes(10)

for i in s:
    print(f"square : ", i)

print("\n")

for t in c:
    print(f"cubes: ", t)