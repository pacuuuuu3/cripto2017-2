#!/usr/bin/python

"""""
Ejecución en Sage:
sage: load('ejercicio4.py')

"""""

# El ejercicio pide los factores primos p y q dado n = 172205490419

# Calcula factores primos de un entero N usando el método de Kraitchik
def kraitchik(n):
    a = ceil(sqrt(n))
    #a = int(math.ceil(math.sqrt(n)))
    b = a*a % n
    while not is_square(b):
        a += 1
        b = a*a % n
    p = a + sqrt(b)
    print("Uno de los factores primos de n es: {0}".format(p))
    print("El cofactor es: {0}".format(int(n/p)))
    print("{0} x {1} = {2}".format(p,int(n/p),n))

n = 172205490419
kraitchik(n)
