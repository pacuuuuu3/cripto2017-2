# Programa que funciona como filtro para los mensajes de correo de Chon Hacker
import hashlib
from base64 import b64encode, b64decode
 
EMOJI1 = bytes("😄", 'utf-8')
EMOJI2 = bytes("😏", 'utf-8')

# Convierte un número a bytes
def to_binary(num):
    return num.to_bytes((num.bit_length() + 7) // 8, 'big')

# Encuentra la cadena apropiada para el filtro de Chon Hacker
def encuentra_cadena(emoji1, emoji2):
    i = 0 # Iterador
    operaciones = 0
    while True:
        cadena = i.to_bytes((i.bit_length() + 7) // 8, 'big')
        crypto = hashlib.sha256(emoji1 + cadena)
        if empieza_emoji(crypto.digest(), emoji2):
            print(operaciones + 3)
            return cadena
        i += 1
        operaciones += 4

# Nos dice si una cadena de bytes comienza con un emoji
def empieza_emoji(cadena, emoji):
    return cadena[:4] == emoji

#PRUEBAS
# print(empieza_emoji(bytes("😎holamundo", 'utf-8'), bytes("😎", 'utf-8'))) 
# print(empieza_emoji(bytes("😂holamundo", 'utf-8'), bytes("😎", 'utf-8')) == False)
# var_prueba = bytes("😂", 'utf-8') + b"\x00\x00\x00\x00\x32\x6a\xc8\x9b"
# cosa = hashlib.sha256(var_prueba).digest()
# print(empieza_emoji(cosa, bytes("😎", 'utf-8')))
# prueba2 = bytes("😄", 'utf-8') +
# cosa2 = hashlib.sha256(prueba2).digest()
# print(empieza_emoji(cosa2, bytes("😏", 'utf-8'))) 
#print(encuentra_cadena(EMOJI1, EMOJI2))

