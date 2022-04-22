from database.connection import create_connection 
from database.setup import User_tbl
from werkzeug.security import generate_password_hash

# registrar usuario 
def insert_user(username, email, password):
    hashed_password = generate_password_hash(password, method='sha256')

    sql = User_tbl.insert().values(email=email, password=hashed_password,username=username, )

    conn = create_connection().connect()
    conn.execute(sql)
    
    conn.close()
