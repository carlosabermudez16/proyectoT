# Dash configuration
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from server import app

# Create app layout
layout = html.Div(children=[
    dcc.Location(id='url_login_df', refresh=True),
    html.Div(
        className="contenedor",
        children=[
            html.Div(
                html.Div(
                    className="fila",
                    children=[
                        html.Div(
                            className="col-lg-10",
                            children=[
                                html.Br(),
                                html.Div('Usuario no autenticado - Por favor inicie sesión para entrar al Dashboard.'),
                            ]
                        ),
                        html.Div(
                            className="col-lg-2",
                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Regresar', n_clicks=0)
                            ]
                        )
                    ]
                )
            )
        ]
    )
])


# Create callbacks
@app.callback(Output('url_login_df', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'
