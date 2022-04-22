from sqlite3 import Error
from .config import Config
from sqlalchemy import create_engine

def create_connection():

    
    try:
        host= Config.host
        user= Config.user
        password= Config.password
        database= Config.database
        
        engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}')

        return engine                         
        
    except Error as e:
        print('Error connecting ti database: ' + str(e))
    
    return engine