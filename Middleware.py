import sys
import socket
import threading
import time
from getIP import get_ipv4
from connection import conectar_base_datos, cerrar_conexion
from modificarBD import *
from Usuario import menu_user
from Admin import menu_admin,menu_admin2,actualizar_sucursales_inactivas
from Ingeniero import menu_ingeniero
from catalogo import determinar_func
import mysql.connector

HEARTBEAT_INTERVAL = 60 #UN minuto
TIMEOUT_INTERVAL = 15
is_master = False
node_status = {}
node_lock = threading.Lock()
master_node = None
coordinator_ip = None

baseDeDatos = None

def main():
    global is_master, master_node, nodes

    # Obtener la dirección IPv4 del host
    ipv4 = get_ipv4()
    global baseDeDatos
    baseDeDatos = conectar_base_datos()

    # Leer las direcciones IP y puertos desde el archivo
    with open("remote_servers.txt", "r") as file:
        nodes = [line.strip().split() for line in file.readlines()]

    node_ips = [ip for ip, port in nodes]
    if ipv4 not in node_ips:
        print("La IP de este nodo no está en la lista de servidores remotos.")
        return

    if nodes[0][0] == ipv4:
        is_master = True
        master_node = ipv4
        print("Este nodo es el nodo maestro.")

    # Iniciar el hilo de heartbeat
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(ipv4, nodes))
    heartbeat_thread.start()

    # Iniciar servidor en un hilo
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

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
            menu_admin(baseDeDatos, coordinator_ip)
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

def send_heartbeat(ipv4, nodes):
    while True:
        try:
            with open("active_nodes.txt", "r") as file:
                previous_active_nodes = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            previous_active_nodes = []
        active_nodes = [ipv4]  # Incluir la propia IP en la lista de nodos activos
        for node_ip, node_port in nodes:
            if node_ip != ipv4:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((node_ip, int(node_port)))
                        s.sendall(b'HEARTBEAT')
                        active_nodes.append(node_ip)
                        with node_lock:
                            node_status[node_ip] = True
                except:
                    with node_lock:
                        node_status[node_ip] = False
                        print(f"Nodo {node_ip} no responde. Redistribuyendo soporte.")
                        redistribute_support(ipv4)
                        if node_ip == master_node:
                            print("Nodo maestro fallido. Iniciando elección de nuevo nodo maestro.")
                            start_election(ipv4, nodes)
        if set(active_nodes) != set(previous_active_nodes):
            print("Cambio detectado en la lista de dispositivos conectados.")
            actualizar_sucursales_inactivas(baseDeDatos)
        
        update_active_nodes_file(active_nodes)
        print("Current active nodes:", active_nodes)

        if active_nodes != previous_active_nodes:
            print("Cambio detectado en la lista de dispositivos conectados.")
            actualizar_sucursales_inactivas(baseDeDatos)
        else:
            print("No hay cambios en la lista de dispositivos conectados.")


        if coordinator_ip not in active_nodes:
            print("El coordinador ya no está activo.")
            #actualizar_sucursales_inactivas(baseDeDatos)
        determine_coordinator_ip()
        time.sleep(HEARTBEAT_INTERVAL)



def update_active_nodes_file(active_nodes):
    with open("active_nodes.txt", "w") as file:
        for node_ip in active_nodes:
            file.write(f"{node_ip}\n")

def determine_coordinator_ip():
    global coordinator_ip
    try:
        with open("active_nodes.txt", "r") as file:
            active_nodes = [line.strip() for line in file.readlines()]
            if active_nodes:
                coordinator_ip = max(active_nodes)
                print(f"Nuevo coordinador IP: {coordinator_ip}")
            else:
                coordinator_ip = None
    except Exception as e:
        print("Error al determinar el coordinador IP:", e)

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
            # Verificar si el mensaje es especial y llamar a la función correspondiente
            determinar_func(baseDeDatos,message)
            if "AGREGAR-MASTER" in message:
                disposAgregar(message,1)
            elif "AGREGAR" in message:
                disposAgregar(message,2)
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

def disposAgregar(data, num):
    try:
        # Dividir el mensaje por comas
        partes = data.split(',')
        palabra_clave = partes[0].strip()
        # Los datos comienzan después de "AGREGAR", así que los recogemos desde la siguiente posición
        datos = [parte.strip() for parte in partes[1:]]
        # Revisar si se proporcionan la cantidad correcta de datos
        if num == 1:
            if len(datos) == 3:
                modelo, marca, anio = datos
                menu_admin2(baseDeDatos, coordinator_ip, modelo, marca, anio)
                print("Entramos a opción 1")
            else:
                print("Cantidad incorrecta de datos para la opción 1")
        elif num == 2:
            if len(datos) == 3:
                modelo, marca, anio = datos
                menu_admin2(baseDeDatos, coordinator_ip, modelo, marca, anio)
                print("Entramos a opción 2")
            else:
                print("Cantidad incorrecta de datos para la opción 2")
    except Exception as e:
        print(f"Error en disposAgregar: {e}")



def save_message(ip_address, message, timestamp):
    with open("messages.txt", "a") as file:
        file.write(f"IP: {ip_address}, Timestamp: {timestamp}, Mensaje: {message}\n")

def print_history():
    try:
        with open("messages.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No se encontró ningún historial de mensajes.")

def redistribute_support(local_ipv4):
    # Implementar lógica para redistribuir tareas
    pass

def start_election(local_ipv4, nodes):
    global master_node, is_master

    higher_nodes = [ip for ip, port in nodes if ip > local_ipv4]
    if not higher_nodes:
        with node_lock:
            is_master = True
            master_node = local_ipv4
        print(f"{local_ipv4} es el nuevo nodo maestro.")
        return

    election_message = f"ELECTION {local_ipv4}"
    for node_ip in higher_nodes:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((node_ip, int(nodes[node_ip])))
                s.sendall(election_message.encode())
        except:
            continue

    timeout = time.time() + TIMEOUT_INTERVAL
    while time.time() < timeout:
        with node_lock:
            if is_master:
                return

    print(f"Ninguna respuesta de nodos superiores. {local_ipv4} es el nuevo nodo maestro.")
    with node_lock:
        is_master = True
        master_node = local_ipv4

if __name__ == "__main__":
    main()
