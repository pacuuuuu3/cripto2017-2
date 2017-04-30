from hashlib import sha1
from base64 import b64encode, b64decode  
import sys
# Programa para saber de qué contraseñas proviene una lista de hashes

#ARCHIVO_HASHES = 'prueba.txt' # Nombre del archivo con los hashes
ARCHIVO_PASSWORDS = 'common-passwords.txt' # Archivo de contraseñas comunes
#ARCHIVO_SALIDA = 'passwords-salt-RESPUESTA.txt' # Nombre del archivo de salida

# Nos dice si el hash proviene de la contraseña con la salt pegada
def proviene_de(password, salt, sha):
    hash_val = sha1((password + salt)).digest()
    return sha == hash_val

hashes = open(sys.argv[1], 'rb') # Abrimos el archivo con el mensaje
lista_hashes = hashes.readlines() # Leemos los hashes
hashes.close()

passwords = open(ARCHIVO_PASSWORDS, 'rb') # Abrimos el archivo con las contraseñas
lista_passwords = passwords.read().splitlines() # Lista con las contraseñas
passwords.close()

correctas = [] # Lista de contraseñas correctas

for sha in lista_hashes:
    salt = sha[1:11]
    has = sha[12:40]
    has = b64decode(has) # Quitamos el encoding
    for password in lista_passwords:
        if(proviene_de(password, salt, has)):
            correctas.append(password)
            break

escritura = open(sys.argv[2], 'wb') # Archivo de salida
for contra in correctas:
    escritura.write(contra + b'\n')
escritura.close()
            
# #PRUEBAS
# hash_val = sha1(('hola' + 'mundo').encode('utf-8')).hexdigest()
# print(proviene_de('hola', 'mundo', hash_val))
# print(hash_val)
