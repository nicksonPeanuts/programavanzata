from copy import copy

def f():
    def g(x):
        return x + 2
    return g


h = f()
print(h(3))

def f(k):
    if k == 1:

        def g(x):
            return x + 2
        return g
    else:
        def h(x):
            return x-2
        return h

h = f(4)
h(7)
h = f(1)
h(7)


def make_adder(n):
    def adder(m):
        return n + m

    return adder


add3 = make_adder(3)
print(add3(2))


def linear(m,q):
    def f(x):
        return m*x + q
    return f

def linear2(m,q):
    return lambda x: m*x + q

# vantaggi? pensare a operazioni che potrei far eseguire da un dizionario, o simili

opcodes = {
    "add": lambda x,y: x + y,
    "sub": lambda x,y: x - y
}

opcodes["add"](2,3)

Y = lambda f: (lambda x: x(x))
(lambda Y: f(lambda *args: y(x)(*args)))

fac = lambda f: lambda n: (1 if n < 2 else n*f(n-1))

Y(fac)(1)
Y(fac)(2)
Y(fac)(3)
Y(fac)(4)
Y(fac)(5)

def list_concat(first):
    def concat(second):
        res = copy(first)
        res.append(second)
        return res
    return concat


x = [1, 2, 3]
c = list_concat(x)
print(c([5, 6, 7]))
x[0] = 12
print(c([5, 6, 7]))
