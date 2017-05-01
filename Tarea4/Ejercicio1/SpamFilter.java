/**
 * Implementación del filtro de Chon Hacker para mensajes spam
 *
 */


import java.security.MessageDigest;
import java.util.Arrays;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.security.SecureRandom;

public class SpamFilter implements Runnable{
    MessageDigest digest; // para manejar los hashes
    byte [] msj_x; // para trabajar en conjunto con los emojis
    byte [] emoji_a; // emoji que se hashea
    byte [] emoji_b; // emoji que se concatena con cualquier cosa
    SecureRandom rand;

    /*acciones para generar un mensaje*/
    enum accion{
	incrementa, // incrementa el valor del byte en el mensaje
	mueve_der, // mueve el byte a la posición derecha del arreglo de bytes 
	mueve_izq, // mueve el byte a la posición izquierda del arreglo de bytes
	copia_der, // copia el valor del byte al byte a su derecha
	copia_izq,  // copia el valor del byte al byte a su izquierda
	cambia_izq, // intercambia el valor del byte con el de su izquierda
	cambia_der // intercambia el valor del byte con el de su derecha
    }
    
    /**
     * Constructor de la clase
     */
    public SpamFilter(){
	try{
	    // queremos calcular hashes de SHA-256
	    this.digest = MessageDigest.getInstance("SHA-256");
	} catch (Exception ex){ex.printStackTrace();}
	// valores en bytes de los emojis por defecto
	emoji_a = new byte[] {(byte)0xF0, (byte)0x9F, (byte)0x98, (byte)0x82};
	emoji_b = new byte[] {(byte)0xF0, (byte)0x9F, (byte)0x98, (byte)0x8E};
	rand = new SecureRandom();
    }

    /**
     * Constructor que recibe dos emojis, 
     * representados como arreglos de bytes y lo asigna a los emojis de la clae
     */
    public SpamFilter(byte[]a, byte[]b){
	try{
	    this.digest = MessageDigest.getInstance("SHA-256");
    	} catch (Exception ex){ex.printStackTrace();}
	emoji_a = a.clone();
	emoji_b = b.clone();
    }


    /**
     * Regresa la representación en hexadecimal de un arreglo de bytes
     */
    public String toHexadecimal(byte [] array){
	StringBuilder sb  = new StringBuilder();
	for (byte b : array)
	    sb.append(String.format("%02X ", b));
	return sb.toString();		
    }

    /*Concatena dos bytes (mensajes) */
    private byte[] byteConcat(byte[]a, byte[] b){
	ByteArrayOutputStream bos = new ByteArrayOutputStream();
	try{
	    bos.write(a);
	    bos.write(b);
	} catch(IOException ioe){ioe.printStackTrace();}
	return bos.toByteArray();
    }
    /**
     * Genera un mensaje aleatorio con longitud aleatoria
     */
    public byte[] nuevoMensaje(){
	/* crea el arreglo de bytes que será el mensaje con una longitud aleatoria*/
	byte [] msj =  new byte[60]; // 60 + 32 bytes = 512 bits
	/* asigna valores aleatorios a cada byte del mensaje*/
	//rand.nextBytes(msj);
	//System.out.println(toHexadecimal(msj));
	for (int i = 0; i < (msj.length*100); i++){
	    accion act = elige_accion();
	    switch(act){
	    case incrementa:
		//System.out.println("Incrementando el byte "+i%msj.length);
		msj[i%msj.length] ^= (0x01 << i%8);
		if(msj[i%msj.length] > 0)
		    System.out.println(msj[i%msj.length]);
		break;
	    case mueve_der:
		//System.out.println("Moviendo a la derecha el byte "+i);
		mueve_der(msj, i%msj.length);
		break;
	    case mueve_izq:
		//System.out.println("Moviendo a la izquierda el byte "+i);
		mueve_izq(msj, i%msj.length);
		break;
	    case copia_der:
		//System.out.println("Copiando a la derecha el byte "+i);
		copia_der(msj, i%msj.length);
		break;
	    case copia_izq:
		//System.out.println("Copiando a la izquierda el byte "+i);
	    case cambia_der:
		//System.out.println("Cambiando a la derecha el byte "+i);
		cambia_der(msj, i%msj.length);
		break;
	    case cambia_izq:
		//System.out.println("Cambiando a la izquierda el byte "+i);
		cambia_izq(msj, i%msj.length);
		break;
	    }
	}
	//System.out.println(toHexadecimal(msj));
	return msj;
    }

    /* 
       mueve el valor de un byte de un arreglo en una posición dada al de su derecha,
       luego, el valor en la posición dada se vuelve 0
    */
    private void mueve_der(byte[] bytes, int pos){
	byte cero = 0x00;
	if(pos >= (bytes.length-1))
	    return;
	bytes[pos+1] = bytes[pos];
	bytes[pos] = cero;
    }

    /*Mueve a la izquierda*/
    private void mueve_izq(byte[] bytes, int pos){
	byte cero = 0x00;
	if(pos <= 0)
	    return;
	bytes[pos-1] = bytes[pos];
	bytes[pos] = cero;
    }
    
    /*copia a la derecha*/
    private void copia_der(byte[] bytes, int pos){
	if (pos >= (bytes.length - 1))
	    return;
	bytes[pos+1] = bytes[pos];
    }

    /*copia a la izquierda*/
    private void copia_izq(byte[] bytes, int pos){
	if (pos <= 0)
	    return;
	bytes[pos-1] = bytes[pos];
    }

    private void swap(byte a, byte b){
	byte tmp = a;
	a = b;
	b = tmp;
    }

    /*intercambia el byte con el de su derecha*/
    private void cambia_der(byte[] bytes, int pos){
	if (pos >= (bytes.length - 1))
	    return;
	swap(bytes[pos], bytes[pos+1]);
    }

    /*intercambia el byte con el de su izquierda*/
    private void cambia_izq(byte[] bytes, int pos){
	if (pos <= 0)
	    return;
	swap(bytes[pos], bytes[pos-1]);
    }

    /*elige una acción aleatoriamente*/
    private accion elige_accion(){
	int sel =  rand.nextInt(accion.values().length);
	return accion.values()[sel];
    }
    
    /**
     * Verifica que el mensaje x generado cumpla con la igualdad
     * SHA256(emoji_a || x) = emoji_b || algo
     */
    public boolean acepta(){
	msj_x = nuevoMensaje();
	//calcula el hash de la concatenación emoji_a || msj_x
	digest.update(byteConcat(emoji_a,msj_x));
	byte[] hash = digest.digest();       
	//System.out.println(toHexadecimal(hash));
	// solo nos interesa ver si el hash inicia con los mismos bytes que el emoji b
	int counter = 0;
	for (int i = 0; i < emoji_b.length; i++){
	    // rechaza si hay algún byte distinto
	    if(hash[i] != emoji_b[i])	       
		return false;	 
	    counter++;
	}	
	return true;
	    
    }
        
    /**
     * Instrucciones para cada hilo de ejecución
     */
    @Override
    public void run(){
	while(!acepta()){} // crea nuevos mensajes aleatorios y los evalua
	System.out.println("Mensaje encontrado!!"+toHexadecimal(msj_x));
	System.exit(0); // termina el programa después de encontrarla
    }

    /*
    * Método principal del programa
    */
    public static void main(String... args){
	int numHilos = 4; // número de hilos de ejecución por defecto
	if (args.length < 1 || args.length > 1)
	    System.out.println("Uso: java SpamFilter <numHilos>");
	else if (args.length == 1){
	    try{
		numHilos = Integer.parseInt(args[0]);
		if (numHilos < 0)
		    numHilos = 4;
	    } catch(NumberFormatException nfe){nfe.printStackTrace();}
	}
	for (int i = 0; i < numHilos; i++){
	    (new Thread(new SpamFilter())).start();
	    System.out.println("Iniciando el hilo "+i);
  	}
	// muestra que se está haciendo algo
	int np = 0;
	System.out.print("Buscando la cadena x ");
	while(true){
	    if (np < 3){
		// imprime un punto
		System.out.print(".");
		np++;
		try {
		    Thread.sleep(1000);  // esperar 1 segundo
		} catch(InterruptedException ex) {
		    Thread.currentThread().interrupt();
		    System.exit(-1);
		}
	    } else {
		// reinicia el número de puntos y se regresa 3 posiciones
		np = 0;
		System.out.print("\b\b\b");
		try{
		    Thread.sleep(1000);
		} catch(InterruptedException ex){
		    Thread.currentThread().interrupt();
		    System.exit(-1);
		}
	    }
	}
    }
}
