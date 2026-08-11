class Cat:

    def __init__(self):
        pass



# semplice CODA In python classe coda
class Queue:
    def __init__(self):
        self.data = []

    def append(self, x):
        self.data.append(x)

    def remove(self):
        x = self.data[0]
        self.data = self.data[1:] # elima il primo elemento della coda. struttura FIFO
        return x
    def empty(self):
        return self.data == []

tom = Cat()
print(tom)

silvestro = Cat()
print(silvestro)
