from Crypto.Cipher import AES
import os

# XOR de bytes. Copiada de Stack Overflow. Créditos al usuario delnan
def bxor(b1, b2): # use xor for bytes
    parts = []
    for b1, b2 in zip(b1, b2):
        parts.append(bytes([b1 ^ b2]))
    return b''.join(parts)

'''
Hace el padding en el mensaje para que su tamaño sea múltiplo de 16 
mensaje - El mensaje al que se le hace padding
'''
def padding(mensaje):
    if len(mensaje) % 16 != 0:
        mensaje += b'\x01'
    while len(mensaje) % 16 != 0:
        mensaje += b'\x00'
    return mensaje
    
''' 
Utilizando la función de AES en ECB, encripta en CBC
mensaje - El mensaje a encriptar
llave - La llave para encriptar 
iv - Vector de inicialización
'''
def encripta_aes_cbc(mensaje, llave, iv):
    mensaje = padding(mensaje)
    i = 0 # Contador
    criptotexto = b'' # Texto cifrado que vamos a regresar
    entrada = iv # Entrada encadenada de la función
    while i < len(mensaje):
        bloque = mensaje[i:i+16] #Bloque a cifrar en AES
        a_cifrar = bxor(entrada, bloque) # XOR de las entradas
        cifrador = AES.new(llave, AES.MODE_ECB) # Cifrador AES
        cifrado = cifrador.encrypt(a_cifrar) # Bloque cifrado
        criptotexto += cifrado        
        entrada = cifrado
        i+=16
    return iv + criptotexto

iv = os.urandom(16) # Vector de inicialización
mensaje = b'hola'
llave = b'Sixteen byte key'
print(encripta_aes_cbc(mensaje,llave, iv))
print(iv + AES.new(llave, AES.MODE_CBC, iv).encrypt(padding(mensaje)))
