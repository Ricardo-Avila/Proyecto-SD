from modificarBD import (
    insertar_datos_usuarios, insertar_datos_ingenieros, insertar_datos_dispositivos, insertar_datos_tickets,
    editar_datos_usuario, editar_datos_ingeniero, editar_datos_dispositivo, editar_datos_ticket,
    eliminar_usuario, eliminar_ingeniero, eliminar_dispositivo, eliminar_ticket
)

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
