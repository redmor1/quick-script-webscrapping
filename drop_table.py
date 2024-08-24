import psycopg2
from psycopg2 import sql


def drop_table(dbname, user, password, table_name, host='localhost', port='5434'):
    """
    Elimina una tabla en PostgreSQL.

    :param dbname: Nombre de la base de datos.
    :param user: Usuario de la base de datos.
    :param password:aseña del usuario de la base de datos.
    :param table_name: Nombre de la tabla a eliminar.
    :param host: Host de la base de datos (por defecto es 'localhost').
    :param port: Puerto de la base de datos (por defecto es '5432').
    """
    try:
        # Conéctate a la base de datos
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Necesario para ejecutar comandos de administración de bases de datos
        cursor = conn.cursor()

        # Ejecut el comando DROP TABLE
        cursor.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name)))
        print(f"Tabla '{table_name}' eliminada exitosamente.")

        # Cierra la conexión
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al eliminar la tabla: {e}")

# Ejemplo de uso
if __name__ == '__main__':
    drop_table('nombre_de_tu_base_de_datos', 'tu_usuario', 'tu_contraseña', 'comercio')
    
drop_table(dbname='postgres', user='postgres', password='admin', table_name='comercio')