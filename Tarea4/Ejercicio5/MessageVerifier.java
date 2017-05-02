public class MessageVerifier{
    private boolean status; // cambia si el mensaje es aceptado

    /**
    * Constructor del verificador de mensajes
    */
    public MessageVerifier(){
	this.status = false;
    }

    /**
     * Regresa el estadod el verificador
     */
    public boolean getStatus(){
	return status;
    }
    /**
     * Verifica que el mensaje generado x cumpla con la igualdad,
     * SHA256(emoji_a || x) = emoji_b || algo
     * @param byte[] msj - el mensaje a verificar
     * @param byte[] emoji - el emoji b
     * @param boolean ready - el generador le avisa si ya terminó
     */
    public synchronized void verificaMensaje(byte [] msj, byte[] emoji, boolean ready){
	if(!ready){
	    try{
		System.out.println("esperando al generador...");
		this.wait();
	    } catch(Exception ex){ex.printStackTrace();}
	}
	int counter = 0; // contador de bytes igualados
	System.out.println("Verificando el mensaje ...");
	for(int i = 0; i < emoji.length; i++){
	    if (msj[i] == emoji[i])
		counter++;
	}
	if (counter > 0)
	    status = true;
    }
}
