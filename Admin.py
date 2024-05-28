from modificarBD import *

def menu_admin(conexion):
    while True:
        print("\nMenú de Administrador:")
        print("1. Ver usuarios")
        print("2. Agregar usuario")
        print("3. Editar usuario")
        print("4. Eliminar usuario")
        print("5. Ver ingenieros")
        print("6. Agregar ingeniero")
        print("7. Editar ingeniero")
        print("8. Eliminar ingeniero")
        print("9. Ver dispositivos")
        print("10. Agregar dispositivo")
        print("11. Editar dispositivo")
        print("12. Eliminar dispositivo")
        print("13. Ver tickets")
        print("14. Eliminar ticket")
        print("15. Consultar folios de tickets")
        print("16. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ver_usuarios(conexion)
        elif opcion == '2':
            insertar_datos_usuarios(conexion, *obtener_datos_usuario())
        elif opcion == '3':
            editar_datos_usuario(conexion, input("Ingresa el ID: "),*obtener_datos_usuario())
        elif opcion == '4':
            eliminar_usuario(conexion, obtener_id())
        elif opcion == '5':
            ver_ingenieros(conexion)
        elif opcion == '6':
            insertar_datos_ingenieros(conexion, *obtener_datos_ingeniero())
        elif opcion == '7':
            editar_datos_ingeniero(conexion, input("Ingresa el ID: "),*obtener_datos_ingeniero())
        elif opcion == '8':
            eliminar_ingeniero(conexion, obtener_id())
        elif opcion == '9':
            ver_dispositivos(conexion)
        elif opcion == '10':
            insertar_datos_dispositivos(conexion, *obtener_datos_dispositivo())
        elif opcion == '11':
            editar_datos_dispositivo(conexion, input("Ingresa el ID: "),*obtener_datos_dispositivo())
        elif opcion == '12':
            eliminar_dispositivo(conexion, obtener_id())
        elif opcion == '13':
            ver_tickets(conexion)
        elif opcion == '14':
            eliminar_ticket(conexion, obtener_id())
        elif opcion == '15':
            consultar_folios(conexion)
        elif opcion == '16':
            print("¡Hasta luego, administrador!")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def obtener_datos_usuario():
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")
    nuevo_correo = input("Nuevo correo electrónico: ")
    nuevo_telefono = input("Nuevo número de teléfono: ")
    return nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono

def obtener_datos_ingeniero():
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")
    anios_experiencia = int(input("Años de experiencia: "))
    nuevo_telefono = input("Nuevo número de teléfono: ")
    return nuevo_nombre, nuevo_apellido, anios_experiencia, nuevo_telefono

def obtener_datos_dispositivo():
    modelo = input("Modelo: ")
    marca = input("Marca: ")
    anio = int(input("Año: "))
    sucursal = int(input("Sucursal: "))
    return modelo, marca, anio, sucursal

def obtener_id():
    return int(input("ID: "))

