from sqlite3 import Error
from .connection import create_connection
from models.tables import User
from sqlalchemy import Table

User_tbl = Table('user', User.metadata) # Se especifica el nombre de la tabla y la metainformación permite hacer el mapeo 
                                        # automático de clase-tabla

def create_tables():
    conn = create_connection() # conectarnos a la base de datos
    print("\nConexión a base de datos exitosa!")
    
    try:
        User.metadata.create_all(conn)    # crea la tabla en la base de datos que se encuentra en la cadena de conexion(url)
        print("Tabla creada exitosamente!\n")
        return True
    except Error as e:
        print(f"Error at create_tables(): {str(e)}" )
    
create_tables()