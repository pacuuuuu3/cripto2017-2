#!/usr/bin/python

# sección a

def a(c,e,n):
    m = 0
    while True:
        if ((m**e)%n == c):
            return m
            #print("m = {0}".format(m))
            #print("{0}^{1} = 10 mod 35".format(m,e))
            #break
        m += 1
print("a) el mensaje claro es: {0}".format(a(10,5,35)))
# sección b
import math

def b(e,n):
        # obtiene los factores primos de n
        p = 3
        q = 1
        for p in range(p,n):
                if (n%p == 0):
                    q = int(n/p)
                    #print("p y q calculados correctamente p = {0}, q = {1}".format(p,q))
                    break
        # calcula d
        p_prime = p - 1
        q_prime = q - 1
        n_prime = p_prime * q_prime
        #print("(p-1)*(q-1) = {0}".format(n_prime))
        d = 1
        while True:
                if ((e*d % n_prime) == 1):
                        return d
                d+=1

print("b) La llave privada d es:{0} ".format(b(31,3599)))

        
        

