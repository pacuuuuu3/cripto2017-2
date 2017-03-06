# Contiene varios métodos de cifrado.
import sys

# César
class Cesar:
    
    # Construye un objeto César a partir de una clave
    def __init__(self, clave):
        if clave < 0:
            raise ValueError('La clave debe estar entre 0 y 255')
        self.clave = clave
        
    # Cifra un conjunto de bytes
    def cifra(self, texto):
        nueva_cadena = [] # Aquí vamos a guardar los bytes cifados
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
        
# Función principal del programa

mensaje_error = 'Para correr el programa: python cifrado.py [c|d] [cesar|afin|mezclado|vigenere] archivoClave archivoEntrada' # Para mensajes de error

try:
    modo = sys.argv[1] # Se lee el modo de uso
    tipo = sys.argv[2] # Se lee el tipo de cifrado a usar
    clave = sys.argv[3] # Se lee el nombre del archivo de la clave
    archiv_ent = sys.argv[4] # Se lee el archivo de entrada
    
    # Aquí vamos a leer la clave
    try:
        archivo = open(clave, 'r') # Abrimos el archivo con la clave
    except:
        print('El archivo con la clave no existe')
    code = archivo.read()
    
    archivo.close()
    # Terminamos de leer la clave. Se guardó en 'code'
    if(tipo == 'cesar'):
        instancia = Cesar(int(code)) # Instancia para cifrar o descifrar
        if(modo == 'c'):
            instancia.cifra_archivo(archiv_ent)
        elif(modo == 'd'):
            instancia.descifra_archivo(archiv_ent)
        else:
            print(mensaje_error)
except:
    print(mensaje_error) 
            
        
