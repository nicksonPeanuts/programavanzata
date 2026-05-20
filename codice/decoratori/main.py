# appunti e prove fatte a lezione


def f():
    k = 1
    while True:
        yield k
        k += 1

def fib():
    a = 0
    b = 1
    result = 0

    while True:
        result = a + b
        a = b
        b = result
        yield b
        

x = fib()

for i in x:
    print(i)
    # forziamo l'uscita
    if i > 100:
        break
