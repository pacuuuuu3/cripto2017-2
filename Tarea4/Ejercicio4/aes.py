from Crypto.Cipher import AES
import os
import re

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
Checa si el mensaje tiene padding
mensaje - El mensaje a checar
'''
def padded(mensaje):
    regexp = re.compile(b'\x01(\x00)*$')
    if regexp.search(mensaje):
        return True
    return False

'''
Quita el padding de una cadena
mensaje - La cadena sobre la que quitaremos el padding
'''
def quita_padding(mensaje):
    mensaje_nuevo = re.sub(b'\x01(\x00)*$', b'', mensaje) # Mensaje a regresar
    return mensaje_nuevo


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
    cifrador = AES.new(llave, AES.MODE_ECB) # Cifrador AES
    while i < len(mensaje):
        bloque = mensaje[i:i+16] #Bloque a cifrar en AES
        a_cifrar = bxor(entrada, bloque) # XOR de las entradas
        cifrado = cifrador.encrypt(a_cifrar) # Bloque cifrado
        criptotexto += cifrado        
        entrada = cifrado
        i+=16
    return iv + criptotexto

'''
Descifra un mensaje encriptado en CBC
mensaje - El mensaje a descifrar
llave - La llave con la cual descifraremos
'''
def descifra_aes_cbc(mensaje, llave):
    mensaje_claro = b'' # El mensaje claro
    iv = mensaje[0:16] # Sacamos el vector de inicialización
    mensaje = mensaje[16:]
    i = 0 # Contador
    descifrador = AES.new(llave, AES.MODE_ECB) # Objeto para descifrar  
    anterior = iv # Variable para descifrar en cadena
    while i < len(mensaje):
        bloque = mensaje[i:i+16] # Bloque a descifrar
        bloque_descifrado = descifrador.decrypt(bloque) # Desciframos el bloque
        bloque_claro = bxor(bloque_descifrado, anterior) # XOR de las entradas
        mensaje_claro += bloque_claro
        anterior = bloque
        i += 16
    return quita_padding(mensaje_claro)
         
#PRUEBAS        
iv = os.urandom(16) # Vector de inicialización
mensaje = b'hola'
llave = b'Sixteen byte key'
print(padded(mensaje))
print(padded(padding(mensaje)))
print(quita_padding(padding(mensaje)))
print(encripta_aes_cbc(mensaje,llave, iv)) 
print(iv + AES.new(llave, AES.MODE_CBC, iv).encrypt(padding(mensaje)))
print(descifra_aes_cbc(encripta_aes_cbc(mensaje, llave, iv), llave))
mensaje = b'\x01x00hola'
print(quita_padding(mensaje))
