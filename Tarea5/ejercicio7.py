# primo sobre el que se construye el campo finito donde estará la curva
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
# coeficientes de la curva
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
# definición de la curva
E =  EllipticCurve(GF(p),[0,0,0,a,b])
# punto generador de la curva
G = E([long(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296),long(0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)])
# clave pública 
Q = E([long(0xcfc746589e4a140785b3bf94c7269ad1b17ad259fbe717c276ae0b0e749833af), long(0x9ee25d020b5be979be4f9367e271322ce8a1006aef0e41f611e7bb1930978ef8)])

# busca k tal que G*k sea Q de manera exhaustiva
k = 1
while (G*k != Q):
    k+=1
print("la clave privada es {0}".format(k))
