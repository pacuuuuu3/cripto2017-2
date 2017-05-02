public class MessageGenerator {

    /*
     * Genera un mensaje para ser verificado
     * @param byte [] msj - el mensaje a modificar
     * @param int it - iteración en la que se genera el mensaje
     * @param boolean ready - señal para el verificador
     */
    public synchronized byte [] generaMensaje(byte [] msj, int it, boolean ready){
	msj[it]+=0x01;
	System.out.println("Nuevo mensaje generado");
	ready = true;
	this.notifyAll();
	return msj;
    }

}
