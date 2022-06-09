import socket
import tqdm
import os

# VARIABLES GLOBALES
SERVER_HOST = "127.0.0.1" # IP del servidor de transferencia
SERVER_PORT = 10000       # El puerto al cual se comunica
BUFFER_SIZE = 4096        # El tamaño de los paquetes es de 4KB
SEPARATOR = "||"          # Bandera que separa el nombre del archivo con el tamaño del mismo




def send_file(filename, SERVER_HOST, SERVER_PORT):

    
    # INFORMACION PREVIA AL ENVIO
    filesize = os.path.getsize(filename)                                    #Obtiene el tamaño del archivo
    
    # ESTABLECER CONEXION
    s = socket.socket()                                                     #Crea el Socket
    
    try:
        print(f"->Estableciendo conexion con {SERVER_HOST}:{SERVER_PORT}...")
        s.connect((SERVER_HOST, SERVER_PORT))                               #Se establece conexion con el servidor
    except:
        print(f"->¡Conexion fallida con {SERVER_HOST}:{SERVER_PORT}!")
        return                                      
    print("->¡Conectado con exito!")
    # ENVIO DE INFORMACION
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())                     #Se envian el nombre y el tamaño como 
                                                                            #"filename"+SEPARATOR+"filesize"
    # BARRA DE PROGRESO DEL ENVIO
    progress = tqdm.tqdm(range(filesize)                                    #Tamaño maximo del Progress_Bar
                        , f"->Enviando... {filename}"                       #Mensaje por consola
                        , unit="B"                                          #Unidad de medida en Bytes
                        , unit_scale=True                                   #Escala
                        , unit_divisor=1024)                                #Tamaño del divisor
    # ENVIO DEL ARCHIVO 
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)                                #Lee 4KB desde el Disco
            if not bytes_read:                                              
                print("¡Transferencia terminada!")                          #Si no se recibe significa que
                break                                                       #termino el envio
        
            s.sendall(bytes_read)                                           #Se envian los bytes leidos
            progress.update(len(bytes_read))                                #Se actualiza el Progress_Bar


    # CERRAR EL SOCKET
    s.close()

if __name__ == "__main__":

    filename = input("nombre y ruta del archivo a subir->")
    send_file(filename, SERVER_HOST, SERVER_PORT)