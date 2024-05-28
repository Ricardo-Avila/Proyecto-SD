import mysql.connector
#Esta funcion nos conecta a la base de datos usando contrasena, usuario y database
def conectar_base_datos():
    try:
        # Establecer conexión a la base de datos en localhost
        conexion = mysql.connector.connect(
            host="localhost",
            user="c0l0mb32",
            password="12345",
            database="SistemasDistribuidos"
        )

        # Verificar si la conexión fue exitosa
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
        else:
            print("Error al conectar a la base de datos")
            return None
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)
        return None
#Se encarga de cerrar correctamente la conexion a la base
def cerrar_conexion(conexion):
    try:
        conexion.close()
        print("Conexión cerrada exitosamente")
    except mysql.connector.Error as error:
        print("Error al cerrar la conexión a la base de datos:", error)

