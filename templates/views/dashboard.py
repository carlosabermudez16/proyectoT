import warnings
warnings.filterwarnings("ignore")   # Es una secuencia de reglas y acciones que coinciden, en este caso ignoras las adevertencias

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_daq as daq
from server import app
from templates.components.graphics import sel3, bar3, sel4, bar4, bar5, fondo_color
from templates.auth.login import header
from templates.components.perfil import perfil
from templates.components.aside_datatable import aside, datatable

app.config.suppress_callback_exceptions = True

app.title = "Control de Asistencia"

layout = html.Div(
    children=[
        
        dcc.Location(id='success', refresh=True),
        
        #fondo_color,
        html.Div([
            html.Div([
                
                
                    
                    fondo_color,
                    # NavBar
                    html.Div([   
                            html.Div([        
                                html.A(html.Img(src=('static/img/logo_dashboard.png')),
                                        href="https://unicesar.edu.co/index.php/es/"),
                                
                                    ],className='col-lg-2 col-md-2',style={'height':'100px','display':'flex','justify-content':'center','align-items':'center'}
                                    ),
                            html.Div([html.H2('Datos de Rendimiento académico'),],className='col-lg-8 col-md-8',style={'height':'100px','display':'flex','justify-content':'center','align-items':'center'}),
                            html.Div([
                                    html.Div([header],
                                            style={'display':'flex','justify-content':'flex-start','flex-wrap':'wrap','font-size':'12px','padding-top':'8px'}),
                                    #html.Br(),
                                    html.Div([
                                        html.Div([
                                        daq.PowerButton(size = 40,labelPosition='left',label='Logout',id='switch',on=True,color="#2cfec1",
                                                        style={'padding-top':'10px'},
                                                        ),], className='col-lg-6'),
                                        html.Div([
                                            perfil
                                        ],className='col-lg-6'),

                                    ],className='col-lg-12'),
                                    ],className='col-lg-2 col-md-2',style={'height':'100px','with':'0px','z-index':'1'}),
                                
                            ],className='flex-display col-lg-12 col-md-12', id= 'header',style={'box-shadow': '2px 2px 2px  #bac7f1'} 
                            ),
                    # Cuerpo
                    html.Div([
                        html.Div([
                            html.Div([
                                            aside, 
                                            
                                            ],className='flex-display',style={'position':'relative'}
                                    ),
                                
                                ],className='flex-display col-lg-3',style={'position':'relative'}
                                ),

                        html.Div([
                            html.Div([
                                    
                                    datatable,
                                    
                                    sel3,
                                    bar3,     
                                    ],className='flex-display col-lg-12',style={'position':'relative'}
                            ),
                            html.Div([
                                    sel4,
                                    bar4,
                                    bar5,
                                ],className='flex-display col-lg-12',style={'position':'relative'}
                            ),
                                ],className='flex-display col-lg-9',style={'position':'relative'}),
                    
                            ],id='dark-theme-provider-demo',className='flex-display col-lg-12',style={'position':'relative'}
                            ),

                
            ],className='fila')
        ], className='contenedor'),
        
        
    ],#style={'background':'#282b38'}
)



@app.callback(
    Output('success', 'pathname'),
    [Input('switch', 'on')])
def update_output(on):
    if on != True:
        from flask_login import logout_user, current_user
        if current_user.is_authenticated:   # is_authenticated regresa un True si el usuario está autenticado
            logout_user()   # Cierra la sesión de un usuario. Esto también limpiará la cookie recordarme si existe.
            return '/'
        else:
            return '\n Nada wey algo esta mal'
        




