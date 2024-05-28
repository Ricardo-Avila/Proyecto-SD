import socket
import threading
import json
from sincronizacion_utils import handle_incoming_message

connected_nodes = []

def initialize_synchronization(local_ipv4):
    with open("remote_servers.txt", "r") as file:
        remote_servers = [line.strip().split() for line in file.readlines() if line.strip().split()[0] != local_ipv4]

    for ip, port in remote_servers:
        connected_nodes.append((ip, int(port)))

def send_update(update_data):
    for ip, port in connected_nodes:
        threading.Thread(target=send_message, args=(ip, port, update_data)).start()

def send_message(ip, port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip, port))
            client_socket.sendall(json.dumps(message).encode())
            print(f"Mensaje enviado a {ip}:{port}: {message}")
    except Exception as e:
        print(f"Error al enviar mensaje a {ip}:{port}:", e)

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
