import socket
import threading
import json
from modificarBD import insertar_datos_usuarios, insertar_datos_ingenieros, insertar_datos_dispositivos, insertar_datos_tickets
from modificarBD import editar_datos_usuario, editar_datos_ingeniero, editar_datos_dispositivo, editar_datos_ticket
from modificarBD import eliminar_usuario, eliminar_ingeniero, eliminar_dispositivo, eliminar_ticket

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

    print(f"Procesando acción: {action} para la tabla: {data['table']}")

    if action == "insert":
        if data["table"] == "usuarios":
            print(f"Insertando usuario: {data['values']}")
            insertar_datos_usuarios(conexion, **data["values"])
        elif data["table"] == "ingenieros":
            print(f"Insertando ingeniero: {data['values']}")
            insertar_datos_ingenieros(conexion, **data["values"])
        elif data["table"] == "dispositivos":
            print(f"Insertando dispositivo: {data['values']}")
            insertar_datos_dispositivos(conexion, **data["values"])
        elif data["table"] == "tickets":
            print(f"Insertando ticket: {data['values']}")
            insertar_datos_tickets(conexion, **data["values"])
    elif action == "update":
        if data["table"] == "usuarios":
            print(f"Actualizando usuario: {data['values']}")
            editar_datos_usuario(conexion, **data["values"])
        elif data["table"] == "ingenieros":
            print(f"Actualizando ingeniero: {data['values']}")
            editar_datos_ingeniero(conexion, **data["values"])
        elif data["table"] == "dispositivos":
            print(f"Actualizando dispositivo: {data['values']}")
            editar_datos_dispositivo(conexion, **data["values"])
        elif data["table"] == "tickets":
            print(f"Actualizando ticket: {data['values']}")
            editar_datos_ticket(conexion, **data["values"])
    elif action == "delete":
        if data["table"] == "usuarios":
            print(f"Eliminando usuario con id: {data['id']}")
            eliminar_usuario(conexion, data["id"])
        elif data["table"] == "ingenieros":
            print(f"Eliminando ingeniero con id: {data['id']}")
            eliminar_ingeniero(conexion, data["id"])
        elif data["table"] == "dispositivos":
            print(f"Eliminando dispositivo con id: {data['id']}")
            eliminar_dispositivo(conexion, data["id"])
        elif data["table"] == "tickets":
            print(f"Eliminando ticket con id: {data['id']}")
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
