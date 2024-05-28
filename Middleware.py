import sys
import socket
import threading
import time
from getIP import get_ipv4
from connection import conectar_base_datos, cerrar_conexion
from modificarBD import insertar_datos_usuarios, insertar_datos_ingenieros, insertar_datos_dispositivos, insertar_datos_tickets
from modificarBD import editar_datos_usuario, editar_datos_ingeniero, editar_datos_dispositivo, editar_datos_ticket
from modificarBD import eliminar_usuario, eliminar_ingeniero, eliminar_dispositivo, eliminar_ticket
from Usuario import menu_user
from Admin import menu_admin
from Ingeniero import menu_ingeniero
from coordinar import initialize_connections, handle_incoming_messages
from Sincronizacion import initialize_synchronization, handle_client, send_update

def main():
    ipv4 = get_ipv4()
    baseDeDatos = conectar_base_datos()
    
    server_thread = threading.Thread(target=start_server, args=(baseDeDatos,))
    server_thread.start()

    initialize_connections(ipv4)
    initialize_synchronization(ipv4)
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

def start_server(conexion):
    try:
        with open("remote_servers.txt", "r") as file:
            server_info = [line.strip().split() for line in file.readlines() if line.strip().split()[0] == get_ipv4()]

        if server_info:
            ip, port = server_info[0]
            port = int(port)
        else:
            print("No se encontró la dirección IP del host en el archivo.")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((ip, port))
            server_socket.listen(5)
            print(f"Servidor con id: {ip} en el puerto {port}")
            while True:
                client_socket, client_address = server_socket.accept()
                connection_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"Conexión entrante de {client_address} a las {connection_time}")
                client_thread = threading.Thread(target=handle_client, args=(client_socket, conexion))
                client_thread.start()
    except Exception as e:
        print("Error al iniciar el servidor:", e)

def connect_to_remote_server(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip, int(port)))
            print(f"Conexión establecida con el servidor remoto en {ip} en el puerto {port}")
            while True:
                time.sleep(1)
    except Exception as e:
        print(f"Error al conectar con el servidor remoto {ip}:{port}:", e)

def connect_to_remote_servers(local_ipv4):
    try:
        with open("remote_servers.txt", "r") as file:
            remote_servers = [line.strip().split() for line in file.readlines() if line.strip().split()[0] != local_ipv4]

        for ip, port in remote_servers:
            thread = threading.Thread(target=connect_to_remote_server, args=(ip, port))
            thread.daemon = True
            thread.start()

        print("Conexiones a servidores remotos iniciadas.")
    except Exception as e:
        print("Error al conectar con los servidores remotos:", e)

def handle_client(client_socket, conexion):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"Conexión entrante desde {client_socket.getpeername()}: {message}")
            handle_incoming_message(message, conexion)
            client_socket.sendall("Mensaje recibido y procesado".encode())
    except Exception as e:
        print("Error al manejar la conexión del cliente:", e)
    finally:
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
