import socket
import tqdm
import os


# VARIABLES GLOBALES
SERVER_HOST = "0.0.0.0" # Escucha todas las IPs
SERVER_PORT = 10000     # El puerto al cual se comunica
BUFFER_SIZE = 4096      # El tamaño de los paquetes es de 4KB
SEPARATOR = "||"        # Bandera que separa el nombre del archivo con el tamaño del mismo
SERVER_LIMIT= 5         # Número maximo de conexiones  



# CREACION DEL SERVER TCP
print("->Creando servidor..")
try:
    s = socket.socket()                 # Creamos el socket
    s.bind((SERVER_HOST, SERVER_PORT))  # Crear el server
    s.listen(5)                         # Establecemos el numero de oyentes
except:
    print("->¡Error al crear el Servidor!")

print("->¡Servidor Creado con exito!")
print(f"->Direccion: {SERVER_HOST},{SERVER_PORT}")


client_socket, address = s.accept() #El servidor espera alguna conexión 


# CONEXION ESTABLECIDA

print(f"->¡[{address}] esta enviando un archivo!")

received = client_socket.recv(BUFFER_SIZE).decode() #Se recibe la informacion del archivo
filename, filesize = received.split(SEPARATOR)      #se conecta usando el socket del cliente
                                                    #Se reciben el nombre y el tamaño como 
                                                    #"filename"+SEPARATOR+"filesize"

filename = os.path.basename(filename)               #Elimina la ruta del archivo dejando el nombre
filesize = int(filesize)                            #como es un str se transforma a int


# BARRA DE PROGRESO DEL ENVIO
progress = tqdm.tqdm(range(filesize)                #Tamaño maximo del Progress_Bar
                    ,f"->Recibiendo... {filename}"     #Mensaje por consola 
                    ,unit="B"                       #Unidad de medida en Bytes
                    ,unit_scale=True                #Escala
                    ,unit_divisor=1024)             #Tamaño del divisor


# RECIBIR EL ARCHIVO                        
with open(filename, "wb") as f:                     #Recibir archivo y se escribe en el disco
    while True:    
        bytes_read = client_socket.recv(BUFFER_SIZE)#Lee 1024 bytes desde el socket
        if not bytes_read:
            print("¡Transferencia terminada!")      #Si no se recibe significa que
            break                                   #termino la transferencia
        
        f.write(bytes_read)                         #Se escribe apenas se reciben los bytes
        progress.update(len(bytes_read))            #Se actualiza el Progress_Bar





# CERRAR EL SERVIDOR
client_socket.close()
s.close()
