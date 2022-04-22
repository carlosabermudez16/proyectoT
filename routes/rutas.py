from flask_login import current_user

from server import app
from dash.dependencies import Input, Output
from templates.auth import login, registro
from templates.auth import  login_fd
from templates.views import dashboard
from dash import dcc
from dash import html

app.layout = html.Div(
    [
        
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='fila'
            ),
        ], className='contenedor'),

        dcc.Location(id='url', refresh=True),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/registro':
            return registro.layout
    elif pathname == '/dashboard':
        if current_user.is_authenticated:   # is_authenticated regresa un True si el usuario está autenticado
            return dashboard.layout
        else:
            return login_fd.layout
    else:
        return '404'
