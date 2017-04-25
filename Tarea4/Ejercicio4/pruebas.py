# Archivo de pruebas
from aes import *
import os
from Crypto.Cipher import AES
import re
    
#PRUEBAS        
iv = os.urandom(16) # Vector de inicialización
mensaje = b'hola'
llave = b'Sixteen byte key'
print(padded(mensaje))
print(padded(padding(mensaje)))
print(quita_padding(padding(mensaje)))

# PRUEBA DE CBC 
print("Prueba CBC")
print(encripta_aes_cbc(mensaje,llave, iv))
print(iv + AES.new(llave, AES.MODE_CBC, iv).encrypt(padding(mensaje)))
print(descifra_aes_cbc(encripta_aes_cbc(mensaje, llave, iv), llave))

print('\n')

# PRUEBA DE OFB
print("Prueba OFB")
print(encripta_aes_ofb(mensaje, llave, iv))
print(iv + AES.new(llave, AES.MODE_OFB, iv).encrypt(padding(mensaje)))
print(descifra_aes_ofb(encripta_aes_ofb(mensaje, llave, iv), llave))

print('\n')

# PRUEBA QUITA PADDING
mensaje = b'\x01x00hola'
print(quita_padding(mensaje))
