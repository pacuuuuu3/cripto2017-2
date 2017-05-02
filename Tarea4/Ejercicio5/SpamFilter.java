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
    MessageGenerator mg;
    MessageVerifier mv;

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
	mg = new MessageGenerator();
	mv = new MessageVerifier();
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

    /*genera un tamaño para el mensaje que sea 60 mod 64 para no tener padding*/
    private int randomSize(){
	int size = 0;
	while(size != 60%64)
	    size = rand.nextInt();
	return size;
    }
        
    /**
     * Instrucciones para cada hilo de ejecución
     */
    @Override
    public void run(){
	byte [] mensaje;
	byte [] hash;
	int i = 0;
	msj_x = new byte[rand.nextInt(20000)];
	boolean ready = false;
	// Corre mientras el verificador no acepte
	while(!mv.getStatus()){
	    System.out.println(toHexadecimal(msj_x));
	    mensaje = byteConcat(emoji_a, mg.generaMensaje(msj_x, i, ready));
	    mv.verificaMensaje(mensaje, emoji_b, ready);
	    i++;
	}
	System.out.println("Mensaje encontrado!!: "+toHexadecimal(msj_x));
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
