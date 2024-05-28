from modificarBD import *

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

def resolver_ticket(conexion, ingeniero_id):
    try:
        cursor = conexion.cursor()

        # Mostrar los tickets asignados al ingeniero
        consultar_ticket_por_id_ingeniero(conexion, ingeniero_id)

        ticket_id = input("Ingrese el ID del ticket que desea resolver: ")
        #estado = input("Ingrese el estado final del ticket (Resuelto, Pendiente, etc.): ")

        # Actualizar el estado del ticket
        cursor.execute("UPDATE TICKETS SET status = %s WHERE id = %s AND ingeniero_id = %s", ("Resuelto", ticket_id, ingeniero_id))
        conexion.commit()
        print("Estado del ticket actualizado correctamente.")

    except mysql.connector.Error as error:
        print("Error al resolver el ticket:", error)


