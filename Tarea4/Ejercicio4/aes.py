from Crypto.Cipher import AES
import os
import re
import sys

#Mensaje de error para cuando el usuario use mal la línea de comandos
MENSAJE_ERROR = "Para correr el programa: python aes.py [c|d] [cbc|ofb] nombre_archivo archivo_clave"

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

'''
Cifra con AES en modo OFB 
mensaje - El mensaje a cifrar
llave - La llave con la cual cifrar
iv - Vector de inicialización
'''
def encripta_aes_ofb(mensaje, llave, iv):
    mensaje = padding(mensaje)
    anterior = iv # Flujo a encriptar
    i = 0 # Contador
    cifrador = AES.new(llave, AES.MODE_ECB) # Instancia cifradora
    criptotexto = b''
    while i < len(mensaje):
        cifrado = cifrador.encrypt(anterior) # Bloque cifrado
        bloque = bxor(cifrado, mensaje[i:i+16]) # Bloque del criptotexto (se le hace xor al cifrado con el mensaje)
        criptotexto += bloque
        i += 16
        anterior = cifrado
    return iv + criptotexto

'''
Descifra un mensaje cifrado con OFB
mensaje - El mensaje a descifrar
llave - La llave con la cual se cifró
'''
def descifra_aes_ofb(mensaje, llave):
    mensaje_claro = b'' # El mensaje claro
    iv = mensaje[0:16] # Sacamos el vector de inicialización
    mensaje = mensaje[16:]
    i = 0 # Contador
    cifrador = AES.new(llave, AES.MODE_ECB) # Objeto para cifrar  
    anterior = cifrador.encrypt(iv) # Variable para descifrar en cadena
    while i < len(mensaje):
        bloque = mensaje[i:i+16] # Bloque a descifrar
        bloque_descifrado = bxor(bloque, anterior) # El bloque se descifra con xor
        mensaje_claro += bloque_descifrado
        anterior = cifrador.encrypt(anterior)
        i += 16
    return quita_padding(mensaje_claro)

# Función principal del programa
try:
    modo = sys.argv[1] # Modo de uso
    modo_aes = sys.argv[2] # Modo para AES
    nombre_archivo = sys.argv[3] # Nombre del archivo con el mensaje
    nombre_clave = sys.argv[4] # Archivo con la clave
    archivo_mensaje = open(nombre_archivo, 'rb') # Abrimos el archivo con el mensaje
    archivo_clave = open(nombre_clave, 'rb') # Abrimos el archivo con la clave
except:
    print(MENSAJE_ERROR)
    sys.exit(-1)
    
mensaje = archivo_mensaje.read() # El mensaje a cifrar/descifrar
archivo_mensaje.close()
clave = archivo_clave.read() # Clave
clave = clave[:16] # Agarro nomás los primeros 16 bytes de la clave
archivo_clave.close()

if modo == 'c':
    escritura = open('cifrado.aes', 'wb')
    if modo_aes == 'cbc':
        escribir = encripta_aes_cbc(mensaje, clave, os.urandom(16))
    elif modo_aes == 'ofb':
        escribir = encripta_aes_ofb(mensaje, clave, os.urandom(16))
    else:
        print(MENSAJE_ERROR)
        sys.exit(-1)
        
elif modo == 'd':
    escritura = open('descifrado.aes', 'wb')
    if modo_aes == 'cbc':
        escribir = descifra_aes_cbc(mensaje, clave)
    elif modo_aes == 'ofb':
        escribir = descifra_aes_ofb(mensaje, clave)
    else:
        print(MENSAJE_ERROR)
        sys.exit(-1)
else:
    print(MENSAJE_ERROR)
    sys.exit(-1)
    
escritura.write(escribir)
escritura.close()


