# index page

from server import app

from database.setup import *

from routes.rutas import *


if __name__ == '__main__':
    #app.config.from_object(debug_mode['development'])
    app.run_server(debug=False)#Config.DEBUG)
