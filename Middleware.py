import sys
import socket
import threading
import time
from getIP import get_ipv4
from connection import conectar_base_datos, cerrar_conexion
from modificarBD import *
from Usuario import menu_user
from Admin import menu_admin
from Ingeniero import menu_ingeniero
from coordinar import initialize_connections, handle_incoming_messages
from Sincronizacion import initialize_synchronization, handle_client

def main():
    # Obtener la dirección IPv4 del host
    ipv4 = get_ipv4()
    baseDeDatos = conectar_base_datos()
    # Iniciar servidor en un hilo
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    
    # Intentar conectarse a los servidores remotos al iniciar el programa
    #threading.Thread(target=connect_to_remote_servers, args=(ipv4,)).start()
    initialize_connections(ipv4)
    threading.Thread(target=handle_incoming_messages).start()

    while True:
        print("\nMenú:")
        print("1. Mostrar historial de mensajes")
        print("2. Acceso Admin")
        print("3. Acceso Usuario")
        print("4. Acceso Ingeniero")
        print("5. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            print("\nHistorial de mensajes:")
            print_history()
        elif choice == '2':
            menu_admin(baseDeDatos)
        elif choice == '3':
            menu_user(baseDeDatos, ipv4)
        elif choice == '4':
            menu_ingeniero(baseDeDatos)
        elif choice == '5':
            print("Saliendo del programa...")
            cerrar_conexion(baseDeDatos)
            sys.exit(0)
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def start_server():
    try:
        # Leer la dirección IP y el puerto correspondiente desde el archivo
        with open("remote_servers.txt", "r") as file:
            server_info = [line.strip().split() for line in file.readlines() if line.strip().split()[0] == get_ipv4()]

        if server_info:
            ip, port = server_info[0]
            port = int(port)
        else:
            print("No se encontró la dirección IP del host en el archivo.")
            return

        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Enlace del socket a la dirección y el puerto
            server_socket.bind((ip, port))
            # Escuchar conexiones entrantes
            server_socket.listen(5)
            print(f"Servidor con id: {ip} en el puerto {port}")
            # Aceptar conexiones entrantes en un bucle infinito
            while True:
                client_socket, client_address = server_socket.accept()
                connection_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"Conexión entrante de {client_address} a las {connection_time}")
                # Manejar la conexión del cliente en un hilo separado
                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                client_thread.start()
    except Exception as e:
        print("Error al iniciar el servidor:", e)

def connect_to_remote_server(ip, port):
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conectar el socket al servidor remoto
            client_socket.connect((ip, int(port)))
            print(f"Conexión establecida con el servidor remoto en {ip} en el puerto {port}")
            # Mantener la conexión abierta sin enviar ni recibir mensajes visibles
            while True:
                time.sleep(1)
    except Exception as e:
        print(f"Error al conectar con el servidor remoto {ip}:{port}:", e)

def connect_to_remote_servers(local_ipv4):
    try:
        # Leer las direcciones IP y puertos desde el archivo
        with open("remote_servers.txt", "r") as file:
            remote_servers = [line.strip().split() for line in file.readlines() if line.strip().split()[0] != local_ipv4]

        # Conectarse a cada servidor remoto en un hilo separado
        for ip, port in remote_servers:
            thread = threading.Thread(target=connect_to_remote_server, args=(ip, port))
            thread.daemon = True  # Permitir que el programa termine aunque estos hilos sigan en ejecución
            thread.start()

        print("Conexiones a servidores remotos iniciadas.")
    except Exception as e:
        print("Error al conectar con los servidores remotos:", e)

def handle_client(client_socket):
    try:
        while True:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if not data:
                break
            # Procesar el mensaje recibido del cliente sin imprimirlo
            message = data.decode()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            # Guardar el mensaje recibido en el archivo de texto
            save_message(client_socket.getpeername()[0], message, timestamp)
            # Si el cliente envía 'exit', salir del bucle y cerrar la conexión
            if message.strip().lower() == 'exit':
                break
            # Enviar de vuelta el mensaje al cliente (eco) sin mostrar en pantalla
            client_socket.sendall("Mensaje recibido".encode())
    except Exception as e:
        print("Error al manejar la conexión del cliente:", e)
    finally:
        # Cerrar el socket del cliente
        client_socket.close()
        print("Conexión con el cliente cerrada.")

def save_message(ip_address, message, timestamp):
    with open("messages.txt", "a") as file:
        file.write(f"IP: {ip_address}, Timestamp: {timestamp}, Mensaje: {message}\n")

def print_history():
    try:
        with open("messages.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No se encontró ningún historial de mensajes.")

if __name__ == "__main__":
    main()
