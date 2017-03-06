# Contiene varios métodos de cifrado.
import sys

# Hacemos división modular (suponiendo que se puede)
def mod_div(int1, int2, modulo):
    for i in range(0, modulo):
        prod = (int2 * i) % modulo # Producto modular
        if prod == int1:
            return i
    raise ValueError('No se puede dividir sobre algo que no sea primo relativo con el módulo')

    
# César
class Cesar:
    
    # Construye un objeto César a partir de una clave
    def __init__(self, clave):
        if clave != (clave % 256):
            raise ValueError('La clave debe estar entre 0 y 255')
        self.clave = clave
        
    # Cifra un conjunto de bytes
    def cifra(self, texto):
        nueva_cadena = [] # Aquí vamos a guardar los bytes cifrados
        for byte in texto:
            byte += self.clave
            byte %= 256
            nueva_cadena.append(bytes([byte]))
        return b''.join(nueva_cadena)

    # Cifra un archivo
    def cifra_archivo(self, nombre_archivo):
        try:
            archivo = open(nombre_archivo, 'rb')
        except:
            print('El archivo a cifrar no existe')
        texto = archivo.read() # Bytes a cifrar
        archivo.close() # Ya no necesitamos el archivo
        cif = self.cifra(texto) # Ciframos el texto
        nombre_salida =  nombre_archivo.split(".")[0] # Nombrar salida
        if self.clave >= 0:
            nombre_salida += '.cifrado'
        else:
            nombre_salida += '.descifrado'
        escritura = open(nombre_salida, 'wb') # Abrimos la salida
        escritura.write(cif)
        escritura.close()

    # Descifra un archivo
    def descifra_archivo(self, nombre_archivo):
        self.clave *= -1 # Descifrar es cifrar con "menos" la clave
        self.cifra_archivo(nombre_archivo)

# Clase para el cifrado Afín
class Afin:

    # Construye un objeto César a partir de un factor y un recorrido 
    def __init__(self, factor, recorrido):
        if factor != (factor % 256):
            raise ValueError('El factor debe estar entre 0 y 255')
        if recorrido != (recorrido % 256):
            raise ValueError('El corrimiento debe estar entre 0 y 255')
        if factor & 1 == 0:
            raise ValueError('El factor debe ser primo relativo con 256')
        self.factor = factor
        self.recorrido = recorrido

    # Cifra un conjunto de bytes
    def cifra(self, texto):
        nueva_cadena = [] # Aquí vamos a guardar los bytes cifrados
        for byte in texto:
            byte *= self.factor
            byte += self.recorrido
            byte %= 256
            nueva_cadena.append(bytes([byte]))
        return b''.join(nueva_cadena)

    # Descifrar sí es distinto de cifrar en este caso
    def descifra(self, texto):
        nueva_cadena = [] # Aquí vamos a guardar los bytes descifrados
        for byte in texto:
            byte -= self.recorrido
            byte = mod_div(byte, self.factor, 256) # División modular
            byte %= 256
            nueva_cadena.append(bytes([byte]))
        return b''.join(nueva_cadena)
    
    # Cifra un archivo
    def cifra_archivo(self, nombre_archivo):
        try:
            archivo = open(nombre_archivo, 'rb')
        except:
            print('El archivo a cifrar no existe')
        texto = archivo.read() # Bytes a cifrar
        archivo.close() # Ya no necesitamos el archivo
        cif = self.cifra(texto) # Ciframos el texto
        nombre_salida =  nombre_archivo.split(".")[0] # Nombrar salida
        nombre_salida += '.cifrado'
        escritura = open(nombre_salida, 'wb') # Abrimos la salida
        escritura.write(cif)
        escritura.close()


    # Descifra un archivo
    def descifra_archivo(self, nombre_archivo):
        try:
            archivo = open(nombre_archivo, 'rb')
        except:
            print('El archivo a descifrar no existe')
        texto = archivo.read() # Bytes a cifrar
        archivo.close() # Ya no necesitamos el archivo
        cif = self.descifra(texto) # Desciframos el texto
        nombre_salida =  nombre_archivo.split(".")[0] # Nombrar salida
        nombre_salida += '.descifrado'
        escritura = open(nombre_salida, 'wb') # Abrimos la salida
        escritura.write(cif)
        escritura.close()


            

class Mezclado:

    # Crea el objeto a partir de una cadena con el alfabeto a usar
    # y los caracteres que  sustituirán a cada uno en el texto cifrado
    def __init__(self, alfabeto, clave):
        # las longitudes deben ser iguales para que el mapeo se haga correctamente
        if len(alfabeto) !=  len(clave):
            raise ValueError('El tamaño del alfabeto y los carácteres a sustituir no coinciden')
        self.alfabeto = alfabeto
        self.clave = clave


        
    def cifra(self, texto):
        cifrado = [] # guarda el texto cifrado 
        for byte in texto:
            # verifica que el byte que se está leyendo esté en el alfabeto
            if byte in self.alfabeto:
                # toma el valor en la clave que corresponde al byte en el alfabeto
                cifrado.append(self.clave[self.alfabeto.index(byte)])
            else:
                print('El carácter ',byte, 'no ha sido encontrado en el alfabeto dado')
        return bytearray(cifrado)


                   
    # Cifra un archivo.
    # La cadena extension indica si estamos cifrando o descrifrando.
    def cifra_archivo(self, nombre_archivo, extension = '.cifrado'):
        try:
            archivo = open(nombre_archivo, 'rb')
        except:
            print('El archivo a cifrar no existe')
        texto = archivo.read() # Bytes a cifrar
        archivo.close() # Ya no necesitamos el archivo
        cif = self.cifra(texto) # Ciframos el texto
        nombre_salida =  nombre_archivo.split(".")[0] # Nombrar salida
        nombre_salida += extension
        escritura = open(nombre_salida, 'wb') # Abrimos la salida
        escritura.write(cif)
        escritura.close()

    # Descifra un archivo
    def descifra_archivo(self, nombre_archivo):
        prov = self.alfabeto # Guardamos el alfabeto por un momento
        self.alfabeto = self.clave
        self.clave = prov
        self.cifra_archivo(nombre_archivo, '.descifrado')

    
mensaje_error = 'Para correr el programa: python cifrado.py [c|d] [cesar|afin|mezclado|vigenere] archivoClave archivoEntrada' # Para mensajes de error

try:
    modo = sys.argv[1] # Se lee el modo de uso
    tipo = sys.argv[2] # Se lee el tipo de cifrado a usar
    clave = sys.argv[3] # Se lee el nombre del archivo de la clave
    archiv_ent = sys.argv[4] # Se lee el archivo de entrada

except IndexError:
    print(mensaje_error)
    sys.exit() # Salimos del programa
    
# Terminamos de leer la clave. Se guardó en 'code'
if(tipo == 'cesar'):

    # Aquí vamos a leer la clave
    try:
        archivo = open(clave, 'r') # Abrimos el archivo con la clave
    except:
        print('El archivo con la clave no existe')

    code = archivo.read() # La clave
    archivo.close()
    instancia = Cesar(int(code)) # Instancia para cifrar o descifrar
    if(modo == 'c'):
        instancia.cifra_archivo(archiv_ent)
    elif(modo == 'd'):
        instancia.descifra_archivo(archiv_ent)
    else:
        print(mensaje_error)

# Terminamos de leer la clave. Se guardó en 'code'
if(tipo == 'afin'):

    # Aquí vamos a leer la clave
    try:
        archivo = open(clave, 'r') # Abrimos el archivo con la clave
    except:
        print('El archivo con la clave no existe')

    code = archivo.readlines() # Las claves
    archivo.close()
    instancia = Afin(int(code[0]), int(code[1])) # Instancia para cifrar o descifrar
    if(modo == 'c'):
        instancia.cifra_archivo(archiv_ent)
    elif(modo == 'd'):
        instancia.descifra_archivo(archiv_ent)
    else:
        print(mensaje_error)


        
# Cifrado y descifrado con el alfabeto mezclado
if (tipo == 'mezclado'):

    # Aquí vamos a leer la clave
    try:
        archivo = open(clave, 'rb') # Abrimos el archivo con la clave
    except:
        print('El archivo con la clave no existe')

    # lee ambas lineas del archivo y asigna los valores en dos variables
    claves = archivo.readlines()
    archivo.close()
    instancia = Mezclado(claves[0], claves[1])    
    if(modo == 'c'):
       instancia.cifra_archivo(archiv_ent)
    elif(modo == 'd'):
        instancia.descifra_archivo(archiv_ent)    

archivo.close() # Creo que esto va aquí           
