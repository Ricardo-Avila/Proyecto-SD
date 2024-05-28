from modificarBD import *
import socket
import random
import mysql.connector

#Muestra un menu con las opciones del ingeniero y con ifs se asegura de ejecutar lo que el ingeniero busque
def menu_ingeniero(conexion):
    # Solicitar al ingeniero que ingrese su ID
    id_ingeniero = input("Por favor, ingrese su ID de ingeniero: ")

    # Consultar al ingeniero por ID
    ingeniero = consultar_ingeniero_por_id(conexion, id_ingeniero)
    # Verificar si se encontró al ingeniero
    if ingeniero:
        print(f"Bienvenido, {ingeniero[1]} {ingeniero[2]}")

        # Mostrar el menú de opciones
        while True:
            print("\nMenú de Ingeniero:")
            print("1. Ver tickets asignados")
            print("2. Resolver ticket asignado")
            print("3. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                consultar_ticket_por_id_ingeniero(conexion, id_ingeniero)
            elif opcion == '2':
                resolver_ticket(conexion, id_ingeniero)
            elif opcion == '3':
                print("¡Hasta luego, ingeniero!")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
    else:
        print("Ingeniero no encontrado. Por favor, verifique su ID.")





def enviar_mensaje_editar_ticket(id_ticket, nueva_descripcion, nuevo_estado, nuevo_ingeniero_id, nuevo_dispositivo_id,sucursal):
    try:
        # Formato del mensaje: "AGREGAR, nombre, apellido, correo, telefono"
        mensaje = f"EDITAR_TICKET,{id_ticket}, {nueva_descripcion}, {nuevo_estado}, {nuevo_ingeniero_id}, {nuevo_dispositivo_id},{sucursal}"

        # Leer las direcciones IP activas desde el archivo servidores_activos.txt
        with open('active_nodes.txt', 'r') as file:
            servidores_activos = file.readlines()

        # Eliminar los saltos de línea (\n) de cada dirección IP
        servidores_activos = [ip.strip() for ip in servidores_activos]

        # Enviar el mensaje a todas las direcciones IP activas
        for ip_destino in servidores_activos:
            enviar_mensaje(ip_destino, obtener_puerto(ip_destino), mensaje)

        print("Mensaje enviado correctamente a todas las direcciones IP activas.")
    except Exception as e:
        print("Error al enviar el mensaje:", e)


def obtener_puerto(ip):
    try:
        with open("remote_servers.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0] == ip:
                    return parts[1]  # Retorna el puerto asociado a la IP
        print(f"No se encontró el puerto asociado a la IP: {ip}")
        return None
    except Exception as e:
        print(f"Error al obtener el puerto de la IP {ip}: {e}")
        return None
#esta funcion manda un mensaje a una ip y su puerto
def enviar_mensaje(ip_destino, puerto_destino, mensaje):
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conectar al servidor destino
            s.connect((ip_destino, int(puerto_destino)))  # Convertir el puerto a entero
            # Enviar el mensaje
            s.sendall(mensaje.encode())
            print(f"Mensaje enviado a {ip_destino}:{puerto_destino}: {mensaje}")
    except Exception as e:
        print(f"Error al enviar mensaje a {ip_destino}:{puerto_destino}: {e}")












def resolver_ticket(conexion, ingeniero_id):
    try:
        cursor = conexion.cursor()

        # Mostrar los tickets asignados al ingeniero
        consultar_ticket_por_id_ingeniero(conexion, ingeniero_id)

        ticket_id = input("Ingrese el ID del ticket que desea resolver: ")
        #estado = input("Ingrese el estado final del ticket (Resuelto, Pendiente, etc.): ")

        
        idTicketOld,usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha, estado,sucursal=consultar_ticket_por_id(conexion, ticket_id)
        enviar_mensaje_editar_ticket(ticket_id, descripcion, "Resuelto", ingeniero_id, dispositivo_id,sucursal)

    except mysql.connector.Error as error:
        print("Error al resolver el ticket:", error)


