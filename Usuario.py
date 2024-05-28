from modificarBD import *
import datetime
import socket
import random
import mysql.connector
#Muestra el menu de el usuario, donde puede abrir tickets
def menu_user(conexion,sucursal):
    # Solicitar al usuario que ingrese su ID
    id_usuario = input("Por favor, ingrese su ID de usuario: ")

    # Consultar el usuario por ID
    usuario = consultar_usuario_por_id(conexion, id_usuario)
    # Verificar si se encontró el usuario
    if usuario:
        print(f"Bienvenido, {usuario[1]} {usuario[2]}")

        # Mostrar el menú de opciones
        while True:
            print("\nMenú:")
            print("1. Ver perfil")
            print("2. Ver dispositivos")
            print("3. Abrir ticket de soporte")
            print("4. Ver tickets")
            print("5. Cerrar sesión")

            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                ver_perfil(usuario)
            elif opcion == '2':
                ver_dispositivos(conexion)
            elif opcion == '3':
                abrir_ticket_soporte(conexion, usuario,input("ID de dispositivo: "),sucursal)
            elif opcion == '4':
                consultar_ticket_por_id_user(conexion, usuario[0])
            elif opcion == '5':
                print("Sesión cerrada. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
    else:
        print("Usuario no encontrado. Por favor, verifique su ID.") 

def ver_perfil(usuario):
    print("Perfil del usuario:")
    print("ID:", usuario[0])
    print("Nombre:", usuario[1])
    print("Apellido:", usuario[2])
    print("Correo:", usuario[3])
    print("Teléfono:", usuario[4])

def editar_perfil(conexion, usuario):
    print("Editar perfil:")
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")
    nuevo_correo = input("Nuevo correo electrónico: ")
    nuevo_telefono = input("Nuevo número de teléfono: ")

    editar_datos_usuario(conexion, usuario[0], nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono)

    print("Perfil actualizado correctamente")


def enviar_mensaje_agregar_ticket(usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha,sucursal):
    try:
        # Formato del mensaje: "AGREGAR, nombre, apellido, correo, telefono"
        mensaje = f"AGREGAR_TICKET,{usuario_id}, {ingeniero_id}, {dispositivo_id}, {descripcion}, {fecha},{sucursal}"

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







def abrir_ticket_soporte(conexion, usuario, id_dispositivo, sucursal):
    print("Crear ticket de soporte:")
    descripcion = input("Descripción del problema: ")

    try:
        cursor = conexion.cursor()

        # Verificar si existe un ticket pendiente para el dispositivo
        cursor.execute("SELECT COUNT(*) FROM TICKETS WHERE dispositivo_id = %s AND status = 'Pendiente'", (id_dispositivo,))
        ticket_pendiente_dispositivo = cursor.fetchone()[0]

        if ticket_pendiente_dispositivo > 0:
            print("Ya existe un ticket pendiente para este dispositivo.")
            return

        # Seleccionar al ingeniero con la menor cantidad de tickets asignados
        cursor.execute("SELECT id FROM INGENIEROS ORDER BY (SELECT COUNT(*) FROM TICKETS WHERE ingeniero_id = INGENIEROS.id) LIMIT 1")
        ingeniero_id = cursor.fetchone()[0]

        fecha = datetime.datetime.now()

        enviar_mensaje_agregar_ticket(usuario[0], ingeniero_id, id_dispositivo, descripcion, fecha,sucursal)
    except mysql.connector.Error as error:
        print("Error al crear ticket de soporte:", error)
    finally:
        cursor.close()


