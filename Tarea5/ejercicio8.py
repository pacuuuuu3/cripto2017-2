"""""
Ejecución en Sage:
sage: load('ejercicio8.py')

"""""

from Crypto.PublicKey import RSA

### Primera llave
k1 = """-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKzl5VggSXb/Jm2oqkPeRQwtpmGlLnJT
Nre4LKx3VUljtLzYWj4xoG+aHBouwJT7DyeibpasCH8Yderr4zIGTNUCAwEAAQ==
-----END PUBLIC KEY-----"""

# Parte pública
pk1 = RSA.importKey(k1)
n1 = pk1.n # modulo del campo
e1 = pk1.e # exponente de la llave pública


### Segunda llave
k2 = """-----BEGIN PUBLIC KEY-----
MF0wDQYJKoZIhvcNAQEBBQADTAAwSQJCAPsrpwx56OTlKtGAWn24bo5HUg3xYtnz
nTj1X/8Hq7pLYNIVE57Yxoyr3zTOOBJufgTNzdKS0Rc5Ti4zZUkCkQvpAgMBAAE=
-----END PUBLIC KEY-----"""

pk2 = RSA.importKey(k2)
n2 = pk2.n
e2 = pk2.e

p = gcd(n1,n2)
q1 = n1/p
q2 = n2/p
print("el factor en común es {0} \n su cofactor en la primera llave es {1} \n su cofactor en la segunda llave es {2}".format(p,q1,q2))


### Para descifrar el mensaje
phi_n = (p-1)*(q1-1)
d1 = inverse_mod(e1,phi_n)
type(d1)
tup = (long(n1),long(e1),long(d1))
privk = RSA.construct(tup)

# mensaje cifrado 
c = 0x41b4e1609390ff8fb5f225b010d1cc79253dcab1744d5f865daabad0e28d259141722382114d9a73106b4d429676dae60a1528a0eb3b73eab0e9d2165c72492f 
m = privk.decrypt(c)
print("el mensaje es {0}".format(m))


