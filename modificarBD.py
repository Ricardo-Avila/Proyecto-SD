from Sincronizacion import *

def obtener_siguiente_id_usuario(conexion):
    try:
        cursor = conexion.cursor()

        # Consulta para obtener el ID más alto de la tabla USUARIOS
        cursor.execute("SELECT MAX(id) FROM USUARIOS")
        max_id = cursor.fetchone()[0]

        # Si no hay usuarios en la tabla, devuelve 1, de lo contrario, devuelve el siguiente ID
        if max_id is None:
            return 1
        else:
            return max_id + 1

    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de usuario:", error)
        return None

def obtener_siguiente_id_ingeniero(conexion):
    try:
        cursor = conexion.cursor()

        # Consulta para obtener el ID más alto de la tabla INGENIEROS
        cursor.execute("SELECT MAX(id) FROM INGENIEROS")
        max_id = cursor.fetchone()[0]

        # Si no hay ingenieros en la tabla, devuelve 1, de lo contrario, devuelve el siguiente ID
        if max_id is None:
            return 1
        else:
            return max_id + 1

    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de ingeniero:", error)
        return None

def obtener_siguiente_id_dispositivo(conexion):
    try:
        cursor = conexion.cursor()

        # Consulta para obtener el ID más alto de la tabla DISPOSITIVOS
        cursor.execute("SELECT MAX(id) FROM DISPOSITIVOS")
        max_id = cursor.fetchone()[0]

        # Si no hay dispositivos en la tabla, devuelve 1, de lo contrario, devuelve el siguiente ID
        if max_id is None:
            return 1
        else:
            return max_id + 1

    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de dispositivo:", error)
        return None

def obtener_siguiente_id_ticket(conexion):
    try:
        cursor = conexion.cursor()

        # Consulta para obtener el ID más alto de la tabla TICKETS
        cursor.execute("SELECT MAX(id) FROM TICKETS")
        max_id = cursor.fetchone()[0]

        # Si no hay tickets en la tabla, devuelve 1, de lo contrario, devuelve el siguiente ID
        if max_id is None:
            return 1
        else:
            return max_id + 1

    except mysql.connector.Error as error:
        print("Error al obtener el siguiente ID de ticket:", error)
        return None


def insertar_datos_usuarios(conexion, nombre, apellido, correo, telefono):
    try:
        cursor = conexion.cursor()
        id = obtener_siguiente_id_usuario(conexion)
        sql_insert_query = """INSERT INTO USUARIOS (id, nombre, apellido, correo, telefono) 
                              VALUES (%s, %s, %s, %s, %s)"""
        valores = (id, nombre, apellido, correo, telefono)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de usuario insertados correctamente")

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

def insertar_datos_ingenieros(conexion,nombre,apellido,aniosExperiencia,telefono):
    try:
        cursor = conexion.cursor()
        id=obtener_siguiente_id_ingeniero(conexion)
        # Ejemplo de inserción de datos en la tabla INGENIEROS
        sql_insert_query = """INSERT INTO INGENIEROS (id, nombre, apellido, aniosExperiencia, telefono) 
                              VALUES (%s, %s, %s, %s, %s)"""
        valores = (id,nombre,apellido,aniosExperiencia,telefono)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de ingeniero insertados correctamente")

    except mysql.connector.Error as error:
        print("Error al insertar datos de ingeniero:", error)

def insertar_datos_dispositivos(conexion, modelo, marca, anio, sucursal):
    try:
        cursor = conexion.cursor()
        id=obtener_siguiente_id_dispositivo(conexion)
        # Ejemplo de inserción de datos en la tabla DISPOSITIVOS
        sql_insert_query = """INSERT INTO DISPOSITIVOS (id, modelo, marca, anio, sucursal) 
                              VALUES (%s, %s, %s, %s, %s)"""
        valores = (id, modelo, marca, anio, sucursal)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de dispositivo insertados correctamente")

    except mysql.connector.Error as error:
        print("Error al insertar datos de dispositivo:", error)

def insertar_datos_tickets(conexion,usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha,sucursal):
    try:
        cursor = conexion.cursor()
        id=obtener_siguiente_id_ticket(conexion)
        # Ejemplo de inserción de datos en la tabla TICKETS
        sql_insert_query = """INSERT INTO TICKETS (id, usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha, sucursal) 
                              VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (id, usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha, sucursal)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Datos de ticket insertados correctamente")

    except mysql.connector.Error as error:
        print("Error al insertar datos de ticket:", error)


def eliminar_usuario(conexion, id_usuario):
    try:
        cursor = conexion.cursor()

        # Ejemplo de eliminación de un usuario de la tabla USUARIOS
        sql_delete_query = "DELETE FROM USUARIOS WHERE id = %s"
        cursor.execute(sql_delete_query, (id_usuario,))
        conexion.commit()
        print("Usuario eliminado correctamente")

    except mysql.connector.Error as error:
        print("Error al eliminar usuario:", error)

def eliminar_ingeniero(conexion, id_ingeniero):
    try:
        cursor = conexion.cursor()

        # Ejemplo de eliminación de un ingeniero de la tabla INGENIEROS
        sql_delete_query = "DELETE FROM INGENIEROS WHERE id = %s"
        cursor.execute(sql_delete_query, (id_ingeniero,))
        conexion.commit()
        print("Ingeniero eliminado correctamente")

    except mysql.connector.Error as error:
        print("Error al eliminar ingeniero:", error)

def eliminar_dispositivo(conexion, id_dispositivo):
    try:
        cursor = conexion.cursor()

        # Ejemplo de eliminación de un dispositivo de la tabla DISPOSITIVOS
        sql_delete_query = "DELETE FROM DISPOSITIVOS WHERE id = %s"
        cursor.execute(sql_delete_query, (id_dispositivo,))
        conexion.commit()
        print("Dispositivo eliminado correctamente")

    except mysql.connector.Error as error:
        print("Error al eliminar dispositivo:", error)

def eliminar_ticket(conexion, id_ticket):
    try:
        cursor = conexion.cursor()

        # Ejemplo de eliminación de un ticket de la tabla TICKETS
        sql_delete_query = "DELETE FROM TICKETS WHERE id = %s"
        cursor.execute(sql_delete_query, (id_ticket,))
        conexion.commit()
        print("Ticket eliminado correctamente")

    except mysql.connector.Error as error:
        print("Error al eliminar ticket:", error)


def consultar_usuario_por_id(conexion, id_usuario):
    try:
        cursor = conexion.cursor()

        # Consultar usuario por ID
        cursor.execute("SELECT * FROM USUARIOS WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()

        return usuario

    except mysql.connector.Error as error:
        print("Error al consultar usuario:", error)
        return None

def consultar_ingeniero_por_id(conexion, id_ingeniero):
    try:
        cursor = conexion.cursor()

        # Consultar ingeniero por ID
        cursor.execute("SELECT * FROM INGENIEROS WHERE id = %s", (id_ingeniero,))
        ingeniero = cursor.fetchone()

        return ingeniero

    except mysql.connector.Error as error:
        print("Error al consultar ingeniero:", error)
        return None

def consultar_dispositivo_por_id(conexion, id_dispositivo):
    try:
        cursor = conexion.cursor()

        # Consultar dispositivo por ID
        cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id_dispositivo,))
        dispositivo = cursor.fetchone()

        return dispositivo

    except mysql.connector.Error as error:
        print("Error al consultar dispositivo:", error)
        return None

def consultar_ticket_por_id(conexion, id_ticket):
    try:
        cursor = conexion.cursor()

        # Consultar ticket por ID
        cursor.execute("SELECT * FROM TICKETS WHERE id = %s", (id_ticket,))
        ticket = cursor.fetchone()
        return ticket

    except mysql.connector.Error as error:
        print("Error al consultar ticket:", error)
        return None

def consultar_ticket_por_id_user(conexion, id_user):
    try:
        cursor = conexion.cursor()

        # Consultar todos los tickets por ID de usuario
        cursor.execute("SELECT * FROM TICKETS WHERE usuario_id = %s", (id_user,))
        tickets = cursor.fetchall()
        
        if tickets:
            print("Tickets encontrados:")
            for ticket in tickets:
                print(ticket)
        else:
            print("No se encontraron tickets para este usuario.")
        
        return tickets

    except mysql.connector.Error as error:
        print("Error al consultar tickets:", error)
        return None


def consultar_ticket_por_id_ingeniero(conexion, ingeniero_id):
    try:
        cursor = conexion.cursor()

        # Consultar los tickets asignados al ingeniero
        cursor.execute("SELECT * FROM TICKETS WHERE ingeniero_id = %s", (ingeniero_id,))
        tickets = cursor.fetchall()

        if tickets:
            print("Tickets asignados:")
            for ticket in tickets:
                print(f"ID: {ticket[0]}, Descripción: {ticket[3]}, Fecha: {ticket[4]}, Estado: {ticket[5]}")
        else:
            print("No hay tickets asignados para resolver.")

    except mysql.connector.Error as error:
        print("Error al obtener los tickets asignados:", error)

def consultar_folios(conexion):
    try:
        cursor = conexion.cursor()

        # Consultar todos los tickets con su sucursal
        cursor.execute("SELECT id, usuario_id, ingeniero_id, sucursal FROM TICKETS")
        tickets = cursor.fetchall()
        
        if tickets:
            print("Folios encontrados:")
            for ticket in tickets:
                id_ticket, id_usuario, id_ingeniero, sucursal = ticket
                folio = generar_folio(id_usuario, id_ingeniero, sucursal, id_ticket)
                print(f"Folio: {folio}")
        else:
            print("No se encontraron tickets.")
        
        return tickets

    except mysql.connector.Error as error:
        print("Error al consultar folios:", error)
        return None

def generar_folio(id_usuario, id_ingeniero, sucursal, id_ticket):
    # Formatea los valores para asegurar que tengan el formato adecuado
    id_usuario = str(id_usuario).zfill(5)
    id_ingeniero = str(id_ingeniero).zfill(5)
    sucursal = sucursal.zfill(15)
    id_ticket = str(id_ticket).zfill(5)
    
    # Concatena los valores para formar el folio
    folio = f"{id_usuario}-{id_ingeniero}-{sucursal}-{id_ticket}"
    return folio




def editar_datos_usuario(conexion, id_usuario, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono):
    try:
        cursor = conexion.cursor()

        # Ejemplo de actualización de datos de usuario en la tabla USUARIOS
        sql_update_query = """UPDATE USUARIOS 
                             SET nombre = %s, apellido = %s, correo = %s, telefono = %s
                             WHERE id = %s"""
        valores = (nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono, id_usuario)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de usuario actualizados correctamente")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de usuario:", error)

def editar_datos_ingeniero(conexion, id_ingeniero, nuevo_nombre, nuevo_apellido, nueva_experiencia, nuevo_telefono):
    try:
        cursor = conexion.cursor()

        # Ejemplo de actualización de datos de ingeniero en la tabla INGENIEROS
        sql_update_query = """UPDATE INGENIEROS 
                             SET nombre = %s, apellido = %s, aniosExperiencia = %s, telefono = %s
                             WHERE id = %s"""
        valores = (nuevo_nombre, nuevo_apellido, nueva_experiencia, nuevo_telefono, id_ingeniero)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de ingeniero actualizados correctamente")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de ingeniero:", error)

def editar_datos_dispositivo(conexion, id_dispositivo, nuevo_modelo, nueva_marca, nuevo_anio, nueva_sucursal):
    try:
        cursor = conexion.cursor()

        # Ejemplo de actualización de datos de dispositivo en la tabla DISPOSITIVOS
        sql_update_query = """UPDATE DISPOSITIVOS 
                             SET modelo = %s, marca = %s, anio = %s, sucursal = %s
                             WHERE id = %s"""
        valores = (nuevo_modelo, nueva_marca, nuevo_anio, nueva_sucursal, id_dispositivo)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de dispositivo actualizados correctamente")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de dispositivo:", error)

def editar_datos_ticket(conexion, id_ticket, nueva_descripcion, nuevo_estado, nuevo_ingeniero_id, nuevo_dispositivo_id):
    try:
        cursor = conexion.cursor()

        # Ejemplo de actualización de datos de ticket en la tabla TICKETS
        sql_update_query = """UPDATE TICKETS 
                             SET descripcion = %s, status = %s, ingeniero_id = %s, dispositivo_id = %s, sucursal = %s
                             WHERE id = %s"""
        valores = (nueva_descripcion, nuevo_estado, nuevo_ingeniero_id, nuevo_dispositivo_id, sucursal, id_ticket)
        cursor.execute(sql_update_query, valores)
        conexion.commit()
        print("Datos de ticket actualizados correctamente")

    except mysql.connector.Error as error:
        print("Error al actualizar datos de ticket:", error)

def ver_usuarios(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM USUARIOS")
        usuarios = cursor.fetchall()
        
        if usuarios:
            print("Usuarios:")
            for usuario in usuarios:
                print(usuario)
        else:
            print("No hay usuarios registrados.")
    except mysql.connector.Error as error:
        print("Error al obtener usuarios:", error)

def ver_ingenieros(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM INGENIEROS")
        ingenieros = cursor.fetchall()
        
        if ingenieros:
            print("Ingenieros:")
            for ingeniero in ingenieros:
                print(ingeniero)
        else:
            print("No hay ingenieros registrados.")
    except mysql.connector.Error as error:
        print("Error al obtener ingenieros:", error)

def ver_dispositivos(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM DISPOSITIVOS")
        dispositivos = cursor.fetchall()
        
        if dispositivos:
            print("Dispositivos:")
            for dispositivo in dispositivos:
                print(dispositivo)
        else:
            print("No hay dispositivos registrados.")
    except mysql.connector.Error as error:
        print("Error al obtener dispositivos:", error)

def ver_tickets(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM TICKETS")
        tickets = cursor.fetchall()
        
        if tickets:
            print("Tickets:")
            for ticket in tickets:
                print(ticket)
        else:
            print("No hay tickets registrados.")
    except mysql.connector.Error as error:
        print("Error al obtener tickets:", error)


