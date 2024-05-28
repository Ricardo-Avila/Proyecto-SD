from modificarBD import *

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
            print("2. Editar perfil")
            print("3. Ver dispositivos")
            print("4. Abrir ticket de soporte")
            print("5. Ver tickets")
            print("6. Cerrar sesión")

            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                ver_perfil(usuario)
            elif opcion == '2':
                editar_perfil(conexion, usuario)
            elif opcion == '3':
                ver_dispositivos(conexion)
            elif opcion == '4':
                abrir_ticket_soporte(conexion, usuario,input("ID de dispositivo: "),sucursal)
            elif opcion == '5':
                consultar_ticket_por_id_user(conexion, usuario[0])
            elif opcion == '6':
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

        # Insertar el nuevo ticket con el ingeniero asignado
        sql_insert_query = """INSERT INTO TICKETS (usuario_id, ingeniero_id, dispositivo_id, descripcion, fecha, status, sucursal) 
                              VALUES (%s, %s, %s, %s, CURRENT_DATE, 'Pendiente', %s)"""
        valores = (usuario[0], ingeniero_id, id_dispositivo, descripcion, sucursal)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Ticket de soporte creado correctamente")
    except mysql.connector.Error as error:
        print("Error al crear ticket de soporte:", error)
    finally:
        cursor.close()
