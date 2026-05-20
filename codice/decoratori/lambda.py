from functools import reduce, partial

f = lambda x: x + 2

print(f(3))

g = lambda x, y: x + 2*y

print(g(3,4))


lst = list(range(20))

map_res = map(lambda x: x + 3, lst)
print(list(map_res))

filter_res = filter(lambda x: x % 2 == 0, lst)
print(list(filter_res))

reduce_res = reduce(lambda x, y: x + y, lst)
print(reduce_res)


def somma(x, y):
    return x + y

def factorial(n):
    return reduce(lambda x, y : x * y, range(1, n+1))



factorial(10)

def prime(n):
    for i in range(2,n):
        if n%i == 0:
            return False
        return True
    
def prime_product(n):
    return reduce(lambda x,y: x * y, filter(prime, n))

somma = partial(somma, 3)
print(somma(5))
