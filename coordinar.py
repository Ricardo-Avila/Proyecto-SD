import socket
import threading
import time
from getIP import get_ipv4

# Lista de nodos conectados (IP y puerto)
connected_nodes = []
coordinator_ip = None

def initialize_connections(local_ipv4):
    try:
        with open("remote_servers.txt", "r") as file:
            remote_servers = [line.strip().split() for line in file.readlines() if line.strip().split()[0] != local_ipv4]

        # Conectarse a cada servidor remoto en un hilo separado
        threads = []
        for ip, port in remote_servers:
            thread = threading.Thread(target=connect_to_remote_server, args=(ip, port))
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        # Iniciar la elección del coordinador después de establecer las conexiones
        start_election(local_ipv4)
    except Exception as e:
        print("Error al conectar con los servidores remotos:", e)

def connect_to_remote_server(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip, int(port)))
            connected_nodes.append((ip, port))
            print("Conexión establecida con el servidor remoto en", ip, "en el puerto", port)
    except Exception as e:
        print(f"Error al conectar con el servidor remoto {ip}:{port}:", e)

def start_election(local_ipv4):
    global coordinator_ip

    print("Iniciando elección del coordinador...")
    highest_ip = local_ipv4
    for ip, port in connected_nodes:
        if ip > highest_ip:
            highest_ip = ip

    if highest_ip == local_ipv4:
        coordinator_ip = local_ipv4
        print("Soy el nuevo coordinador:", coordinator_ip)
        notify_nodes("COORDINATOR", coordinator_ip)
    else:
        coordinator_ip = highest_ip
        print("El nuevo coordinador es:", coordinator_ip)

def notify_nodes(message, coordinator_ip):
    for ip, port in connected_nodes:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, int(port)))
                client_socket.sendall(f"{message} {coordinator_ip}".encode())
        except Exception as e:
            print(f"Error al notificar al nodo {ip}:{port}:", e)

def handle_incoming_messages():
    while True:
        # Este código debe manejar la recepción de mensajes de otros nodos
        # para actualizar el coordinador cuando se reciba un mensaje COORDINATOR.
        pass

if __name__ == "__main__":
    local_ipv4 = get_ipv4()
    initialize_connections(local_ipv4)
    threading.Thread(target=handle_incoming_messages).start()
