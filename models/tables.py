from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   # se crea el objeto 

# la clase User representa  a los usuarios de nuestra aplicación
class User(db.Model):   # Model es un atributo que abilita todas las funcionalidades de la clase SQLAlchemy.
    id = db.Column(db.Integer, primary_key=True)    # campo id entero, se incrementa automáticamente y se toma como clave primaria
    username = db.Column(db.String(15), unique=True)    # columna con nombre username string
    email = db.Column(db.String(50), unique=True)   # columna con nombre email string
    password = db.Column(db.Text) # columna con nombre password string


