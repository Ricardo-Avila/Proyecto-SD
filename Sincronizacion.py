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
