# Dash app initialization
import dash
# User management initialization
import os
from flask_login import LoginManager, UserMixin
from models.tables import db, User as base


from database.config import Config


app = dash.Dash(
    __name__,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ],
)
server = app.server # Exponemos la variable server para agregar y configurar implemtaciones
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Actualiza la base de datos siempre que se inicie el servidor
server.config.update(
    SECRET_KEY=os.urandom(12),  # se establece la variable de configuración, genera un token que sirve para proteger la aplicación de ataques 
    SQLALCHEMY_DATABASE_URI= f'mysql+mysqlconnector://{Config.user}:{Config.password}@{Config.host}:3306/{Config.database}', # configuramos para que exista una conexión entre el ORM y la base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


db.init_app(server) # inicializa la base de datos en conjunto con la aplicación

# 
login_manager = LoginManager()  #  Un cargador de usuario indica a Flask-Login cómo encontrar un usuario específico a partir del 
                                # identificador que se almacena en su cookie de sesión
login_manager.init_app(server)  # configurarción para iniciar sesión 
login_manager.login_view = '/login' # si un usuario intenta acceder a una vista protegida esto lo redirecciona a la pagina de login



#  El UserMixin añadirá atributos de Flask-Login al modelo de forma que Flask-Login pueda trabajar con él.
class User(UserMixin, base):
    pass


# Devolución de llamada para recargar el objeto de usuario desde el ID de 
# usuario almacenado en la sección
@login_manager.user_loader  # método user_loader nos permite acceder desde nuestro código al usuario cuyo ID se encuentra almacenado en la base de datos
def load_user(user_id):
    return User.query.get(int(user_id)) # query permite hacer consulta a la base de datos, pero para ejecutarse sobre la base de datos
                                        # se le debe indicar la opreación a realizar.
                                        # get() devuelve un objeto del tipo indicado en la Query a partir de su primary_key. 
                                        # Si no encuentra el objeto, devuelve None.
