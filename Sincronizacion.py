import socket
import threading
import json
import mysql.connector

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
            insertar_datos_usuarios(conexion, **data["values"], send_update=False)
        elif data["table"] == "ingenieros":
            print(f"Insertando ingeniero: {data['values']}")
            insertar_datos_ingenieros(conexion, **data["values"], send_update=False)
        elif data["table"] == "dispositivos":
            print(f"Insertando dispositivo: {data['values']}")
            insertar_datos_dispositivos(conexion, **data["values"], send_update=False)
        elif data["table"] == "tickets":
            print(f"Insertando ticket: {data['values']}")
            insertar_datos_tickets(conexion, **data["values"], send_update=False)
    elif action == "update":
        if data["table"] == "usuarios":
            print(f"Actualizando usuario: {data['values']}")
            editar_datos_usuario(conexion, **data["values"], send_update=False)
        elif data["table"] == "ingenieros":
            print(f"Actualizando ingeniero: {data['values']}")
            editar_datos_ingeniero(conexion, **data["values"], send_update=False)
        elif data["table"] == "dispositivos":
            print(f"Actualizando dispositivo: {data['values']}")
            editar_datos_dispositivo(conexion, **data["values"], send_update=False)
        elif data["table"] == "tickets":
            print(f"Actualizando ticket: {data['values']}")
            editar_datos_ticket(conexion, **data["values"], send_update=False)
    elif action == "delete":
        if data["table"] == "usuarios":
            print(f"Eliminando usuario con id: {data['id']}")
            eliminar_usuario(conexion, data["id"], send_update=False)
        elif data["table"] == "ingenieros":
            print(f"Eliminando ingeniero con id: {data['id']}")
            eliminar_ingeniero(conexion, data["id"], send_update=False)
        elif data["table"] == "dispositivos":
            print(f"Eliminando dispositivo con id: {data['id']}")
            eliminar_dispositivo(conexion, data["id"], send_update=False)
        elif data["table"] == "tickets":
            print(f"Eliminando ticket con id: {data['id']}")
            eliminar_ticket(conexion, data["id"], send_update=False)

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

# Definir las funciones que eran parte de modificarBD.py para manipular la base de datos
def insertar_datos_usuarios(conexion, nombre, apellido, correo, telefono, send_update=True):
    try:
        cursor = conexion.cursor()
        id = obtener_siguiente_id_usuario(conexion)
        sql_insert_query = """INSERT INTO USUARIOS (id, nombre, apellido, correo, telefono) 
                              VALUES (%s, %s, %s, %s, %s)"""
        valores = (id, nombre, apellido, correo, telefono)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de usuario insertados correctamente")

        if send_update:
            # Enviar actualización a otros nodos
            update_data = {
                "action": "insert",
                "data": {
                    "table": "usuarios",
                    "values": {
                        "id": id,
                        "nombre": nombre,
                        "apellido": apellido,
                        "correo": correo,
                        "telefono": telefono
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al insertar datos de usuario:", error)

# (Definir de manera similar las funciones insertar_datos_ingenieros, insertar_datos_dispositivos, insertar_datos_tickets)
def insertar_datos_ingenieros(conexion, nombre, apellido, aniosExperiencia, telefono, send_update=True):
    try:
        cursor = conexion.cursor()
        id = obtener_siguiente_id_ingeniero(conexion)
        sql_insert_query = """INSERT INTO INGENIEROS (id, nombre, apellido, aniosExperiencia, telefono) 
                              VALUES (%s, %s, %s, %s, %s)"""
        valores = (id, nombre, apellido, aniosExperiencia, telefono)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de ingeniero insertados correctamente")

        if send_update:
            update_data = {
                "action": "insert",
                "data": {
                    "table": "ingenieros",
                    "values": {
                        "id": id,
                        "nombre": nombre,
                        "apellido": apellido,
                        "aniosExperiencia": aniosExperiencia,
                        "telefono": telefono
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al insertar datos de ingeniero:", error)

def insertar_datos_dispositivos(conexion, modelo, marca, anio, sucursal, send_update=True):
    try:
        cursor = conexion.cursor()
        id = obtener_siguiente_id_dispositivo(conexion)
        sql_insert_query = """INSERT INTO DISPOSITIVOS (id, modelo, marca, anio, sucursal) 
                              VALUES (%s, %s, %s, %s, %s)"""
        valores = (id, modelo, marca, anio, sucursal)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de dispositivo insertados correctamente")

        if send_update:
            update_data = {
                "action": "insert",
                "data": {
                    "table": "dispositivos",
                    "values": {
                        "id": id,
                        "modelo": modelo,
                        "marca": marca,
                        "anio": anio,
                        "sucursal": sucursal
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al insertar datos de dispositivo:", error)

def insertar_datos_tickets(conexion, usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha, sucursal, send_update=True):
    try:
        cursor = conexion.cursor()
        id = obtener_siguiente_id_ticket(conexion)
        sql_insert_query = """INSERT INTO TICKETS (id, usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha, sucursal) 
                              VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (id, usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha, sucursal)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de ticket insertados correctamente")

        if send_update:
            update_data = {
                "action": "insert",
                "data": {
                    "table": "tickets",
                    "values": {
                        "id": id,
                        "usuario_id": usuario_id,
                        "ingeniero_id": ingeniero_id,
                        "dispositivo_id": dispositivo_id,
                        "descripcion": descripcion,
                        "fecha": fecha,
                        "sucursal": sucursal
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al insertar datos de ticket:", error)

def editar_datos_usuario(conexion, id, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_update_query = """UPDATE USUARIOS 
                             SET nombre = %s, apellido = %s, correo = %s, telefono = %s
                             WHERE id = %s"""
        valores = (nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono, id)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de usuario actualizados correctamente")

        if send_update:
            update_data = {
                "action": "update",
                "data": {
                    "table": "usuarios",
                    "values": {
                        "id": id,
                        "nombre": nuevo_nombre,
                        "apellido": nuevo_apellido,
                        "correo": nuevo_correo,
                        "telefono": nuevo_telefono
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de usuario:", error)

# (Definir de manera similar las funciones editar_datos_ingeniero, editar_datos_dispositivo, editar_datos_ticket)
def editar_datos_ingeniero(conexion, id, nombre, apellido, aniosExperiencia, telefono, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_update_query = """UPDATE INGENIEROS 
                             SET nombre = %s, apellido = %s, aniosExperiencia = %s, telefono = %s
                             WHERE id = %s"""
        valores = (nombre, apellido, aniosExperiencia, telefono, id)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de ingeniero actualizados correctamente")

        if send_update:
            update_data = {
                "action": "update",
                "data": {
                    "table": "ingenieros",
                    "values": {
                        "id": id,
                        "nombre": nombre,
                        "apellido": apellido,
                        "aniosExperiencia": aniosExperiencia,
                        "telefono": telefono
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de ingeniero:", error)

def editar_datos_dispositivo(conexion, id, modelo, marca, anio, sucursal, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_update_query = """UPDATE DISPOSITIVOS 
                             SET modelo = %s, marca = %s, anio = %s, sucursal = %s
                             WHERE id = %s"""
        valores = (modelo, marca, anio, sucursal, id)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de dispositivo actualizados correctamente")

        if send_update:
            update_data = {
                "action": "update",
                "data": {
                    "table": "dispositivos",
                    "values": {
                        "id": id,
                        "modelo": modelo,
                        "marca": marca,
                        "anio": anio,
                        "sucursal": sucursal
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de dispositivo:", error)

def editar_datos_ticket(conexion, id, descripcion, status, ingeniero_id, dispositivo_id, sucursal, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_update_query = """UPDATE TICKETS 
                             SET descripcion = %s, status = %s, ingeniero_id = %s, dispositivo_id = %s, sucursal = %s
                             WHERE id = %s"""
        valores = (descripcion, status, ingeniero_id, dispositivo_id, sucursal, id)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de ticket actualizados correctamente")

        if send_update:
            update_data = {
                "action": "update",
                "data": {
                    "table": "tickets",
                    "values": {
                        "id": id,
                        "descripcion": descripcion,
                        "status": status,
                        "ingeniero_id": ingeniero_id,
                        "dispositivo_id": dispositivo_id,
                        "sucursal": sucursal
                    }
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de actualización: {update_data}")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de ticket:", error)

def eliminar_usuario(conexion, id, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_delete_query = "DELETE FROM USUARIOS WHERE id = %s"
        cursor.execute(sql_delete_query, (id,))
        conexion.commit()
        print("Usuario eliminado correctamente")

        if send_update:
            update_data = {
                "action": "delete",
                "data": {
                    "table": "usuarios",
                    "id": id
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de eliminación: {update_data}")

    except mysql.connector.Error as error:
        print("Error al eliminar usuario:", error)

# (Definir de manera similar las funciones eliminar_ingeniero, eliminar_dispositivo, eliminar_ticket)
def eliminar_ingeniero(conexion, id, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_delete_query = "DELETE FROM INGENIEROS WHERE id = %s"
        cursor.execute(sql_delete_query, (id,))
        conexion.commit()
        print("Ingeniero eliminado correctamente")

        if send_update:
            update_data = {
                "action": "delete",
                "data": {
                    "table": "ingenieros",
                    "id": id
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de eliminación: {update_data}")

    except mysql.connector.Error as error:
        print("Error al eliminar ingeniero:", error)

def eliminar_dispositivo(conexion, id, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_delete_query = "DELETE FROM DISPOSITIVOS WHERE id = %s"
        cursor.execute(sql_delete_query, (id,))
        conexion.commit()
        print("Dispositivo eliminado correctamente")

        if send_update:
            update_data = {
                "action": "delete",
                "data": {
                    "table": "dispositivos",
                    "id": id
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de eliminación: {update_data}")

    except mysql.connector.Error as error:
        print("Error al eliminar dispositivo:", error)

def eliminar_ticket(conexion, id, send_update=True):
    try:
        cursor = conexion.cursor()
        sql_delete_query = "DELETE FROM TICKETS WHERE id = %s"
        cursor.execute(sql_delete_query, (id,))
        conexion.commit()
        print("Ticket eliminado correctamente")

        if send_update:
            update_data = {
                "action": "delete",
                "data": {
                    "table": "tickets",
                    "id": id
                }
            }
            send_update(update_data)
            print(f"Enviado mensaje de eliminación: {update_data}")

    except mysql.connector.Error as error:
        print("Error al eliminar ticket:", error)

# Las funciones para obtener el siguiente ID
def obtener_siguiente_id_usuario(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(id) FROM USUARIOS")
        max_id = cursor.fetchone()[0]
        return 1 if max_id is None else max_id + 1
    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de usuario:", error)
        return None

def obtener_siguiente_id_ingeniero(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(id) FROM INGENIEROS")
        max_id = cursor.fetchone()[0]
        return 1 if max_id is None else max_id + 1
    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de ingeniero:", error)
        return None

def obtener_siguiente_id_dispositivo(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(id) FROM DISPOSITIVOS")
        max_id = cursor.fetchone()[0]
        return 1 if max_id is None else max_id + 1
    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de dispositivo:", error)
        return None

def obtener_siguiente_id_ticket(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(id) FROM TICKETS")
        max_id = cursor.fetchone()[0]
        return 1 if max_id is None else max_id + 1
    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de ticket:", error)
        return None
