#!/usr/bin/python

# Encuentra los factores primos usando el algoritmo ro de Pollard
# El ejercicio pide los factores p y q dado n = 172205490419
import math
import threading
import gmpy2

# Calcula el máximo común divisor de dos números
def mcd(a,b):
    if (a == 0):
        return b
    return mcd(b%a,a)

# Calcula factores primos de un entero N usando el método de Kraitchik
def kraitchik(n):
    a = int(math.ceil(math.sqrt(n)))
    b = a*a % n
    while not gmpy2.is_square(b):
        a += 1
        b = a*a % n
    p = a + int(math.sqrt(b))
    print("Uno de los factores primos de n es: {0}".format(p))
    print("El cofactor es: {0}".format(int(n/p)))
    print("{0} x {1} = {2}".format(p,int(n/p),n))

n = 172205490419
kraitchik(n)
