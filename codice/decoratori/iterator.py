# classe per insieme generico
class MySet:

    def __init__(self):
        self._data = []

    def add(self, x):
        if x not in self._data:
            # self._data.append(x)
            self._data = [x] + self.data

    def __iter__(self):
        self._pos = 0
        self._max_elems = len(self._data)
        return self

    def __next__(self):
        # posizione più grande della lunghezza dei dati! no posible
        if self._pos >= self._max_elems:
            raise StopIteration
        else:
            res = self._data[self._pos]
            self._pos += 1
            return res



# iteratore di cubi
class Cubes:
    def __init__(self, max_cubes):
        self.max_cubes = max_cubes

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n > self.max_cubes:
            raise StopIteration
        else:
            res = self.n**3
            self.n += 1
            return res
        



s = MySet()
s.add(100)
s.add(89)
s.add(42)

for x in s:
    print(x)

x = iter(s)
print(next(x))

print("\n CUBES \n")

c = Cubes(10)
for x in c:
    print(x)