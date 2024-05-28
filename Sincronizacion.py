import socket
import threading
import json
from modificarBD import *

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

def handle_incoming_message(message, conexion):
    print(f"Mensaje recibido: {message}")
    update_data = json.loads(message)
    action = update_data["action"]
    data = update_data["data"]

    if action == "insert":
        if data["table"] == "usuarios":
            insertar_datos_usuarios(conexion, **data["values"])
        elif data["table"] == "ingenieros":
            insertar_datos_ingenieros(conexion, **data["values"])
        elif data["table"] == "dispositivos":
            insertar_datos_dispositivos(conexion, **data["values"])
        elif data["table"] == "tickets":
            insertar_datos_tickets(conexion, **data["values"])
    elif action == "update":
        if data["table"] == "usuarios":
            editar_datos_usuario(conexion, **data["values"])
        elif data["table"] == "ingenieros":
            editar_datos_ingeniero(conexion, **data["values"])
        elif data["table"] == "dispositivos":
            editar_datos_dispositivo(conexion, **data["values"])
        elif data["table"] == "tickets":
            editar_datos_ticket(conexion, **data["values"])
    elif action == "delete":
        if data["table"] == "usuarios":
            eliminar_usuario(conexion, data["id"])
        elif data["table"] == "ingenieros":
            eliminar_ingeniero(conexion, data["id"])
        elif data["table"] == "dispositivos":
            eliminar_dispositivo(conexion, data["id"])
        elif data["table"] == "tickets":
            eliminar_ticket(conexion, data["id"])

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
