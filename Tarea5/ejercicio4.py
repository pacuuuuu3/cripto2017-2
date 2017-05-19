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

# Regresa un polinomio de la forma g(x) = (x^2 - 1) mod n
def g1(x,n):
    return ((x**2)-1) % n

# Regresa un polinomio de la forma g(x) = (x^2 + 1) mod n
def g2(x,n):
    return ((x**2)+1) % n

# Algoritmo de Pollard
def rho(n, g):
    x = 2 # valor inicial de x_i
    y = 2 # valor inicial de x_j
    d = 1 # divisor
    while d == 1: 
        x = g(x,n)
        #print("x_i es {0}".format(x))
        y = g(g(x,n),n)
        #print("x_j es {0}".format(y))
        d = mcd(int(math.fabs(x-y)),n)
        # print(d)
    if ( d == n):
        print("error al buscar factores primos: no se encontraron divisores de n = {0}".format(n))
    else:
        print("el primer factor es: {0}".format(d))
        print("el cofactor es: {0}". format(n/d))


# Calcula factores primos de un entero N usando el método de Kraitchik
def kraitchik(n):
    a = int(math.ceil(math.sqrt(n)))
    b = a*a % n
    while not gmpy2.is_square(b):
        a += 1
        b = a*a % n
        print("kraitchick en: {0}".format(a))
    p = a + int(math.sqrt(b))
    print("Uno de los factores primos de n es: {0}".format(p))
    print("El cofactor es: {0}".format(int(n/p)))
    print("{0} x {1} = {2}".format(p,int(n/p),n))

n = 172205490419
kraitchik(n)

# Crea un hilo de ejecución por cada función g
#t1 = threading.Thread(target=rho,args=(n,g1))
#t2 = threading.Thread(target=rho,args=(n,g2))
# hilos para kraitchik
#t3 = threading.Thread(target=kraitchik,args=(n,))
# Inicia los hilos
#t1.start()
#t2.start()
#t3.start()
# espera a que terminen los hilos
#t1.join()
#t2.join()
#t3.join()
