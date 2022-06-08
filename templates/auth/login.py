from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from server import app, User
from flask_login import login_user,current_user # Este current_user representa al usuario de la base de datos, y podemos acceder a todos los atributos de ese usuario con notación por puntos.
from werkzeug.security import check_password_hash

app.title = "Inicio de sesión"

header = html.Div(
    className='username',

    children=html.Div(
        className='contenedor',
        
        children=[
            
            html.Div(
                children=[
                    html.Div(id='user-name'),
                    ]
                    ),

            html.Div(id='page-content'),
        ]
    )

)

layout = html.Div(
    
    children=[
        # fondo
        
        html.Div([
            html.Div(id='fondo1'),
            html.Div(id='fondo2'),
            html.Div(id='fondo3'),
            html.Div(id='fondo4'),
        ]),
                
        #Logo
        html.Div([
                    html.Div([
                        html.Div([html.P('_'),],className='col-lg-1 col-md-1 col-sm-1',style={'color':'rgba(255,255,255,0)'}),
                        html.Div([    
                            
                            html.Img(src='static/img/logo2.png',className='LOGO'),
                            html.H1(id='titulo',
                                children='Universidad Popular del Cesar')
                            ],className='col-lg-10 col-md-10 col-sm-10 col-xs-12', id='orden',
                            ),
                        html.Div([html.P('_'),],className='col-lg-1 col-md-1 col-sm-1',style={'color':'rgba(255,255,255,0)'}),
                    ],className='fila'),
                ],className='contenedor'
            ),
        # Formulario
        html.Div(
            
            children=[
                html.Div([
                    dcc.Location(id='url_login', refresh=True),

                    html.Div([ html.H1('_')],className='col-lg-4 col-md-4 col-sm-4',style={'color':'rgba(255,255,255,0)',
                                            'background':'transparent'}),
                    
                    html.Div(
                        # method='Post',
                        children=[
                            html.H1('Login Form',style={'font-size':'30px'}, id='titulo2'),
                            html.Br(),
                            dcc.Input(
                                placeholder='Correo electrónico',
                                n_submit=0,
                                type='email',
                                id='input_email'
                            ),
                            html.Br(),
                            dcc.Input(
                                placeholder='Password',
                                n_submit=0,
                                type='password',
                                id='input_password'
                            ),
                            html.Br(),
                            html.A('Forgot password', href='https://www.youtube.com/',
                                                                style = {   
                                                                            "text-align": "center",
                                                                            'font-size': '14px',
                                                                            'margin-bottom':'5%',
                                                                            }),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                html.A(html.Button(
                                    children='Register',
                                    n_clicks=0,
                                    type='submit',
                                    id='btn3',
                                    className='col-lg-4'
                                ),href='/registro'),
                                html.Div([ html.H1('_')],className='col-lg-4 col-md-4 col-sm-4',style={'color':'rgba(255,255,255,0)',
                                            'background':'transparent'}),
                                html.Button(
                                    children='Login',
                                    n_clicks=0,
                                    type='submit',
                                    id='btn4',
                                    className='col-lg-4'
                                ),
                            ],className='col-lg-12',style={'background':'red'}
                            ),

                            html.Div(children='', id='output-state')

                            
                            ],className='col-lg-4',id='orden1',style={'text-align': 'center'}
                        ),#'background':'rgba(200,20,20,.5)'}),
                
                    html.Div([ html.H1('_')],className='col-lg-4 col-md-4 col-sm-4',style={'color':'rgba(255,255,255,0)',
                                            'background':'transparent'}),
                ],className='fila'),
            ],className="contenedor",
        ),
        
        # pie de página
        
        html.Div([
            html.Div([
                html.Div([
                            html.Div([
                                html.P(['© Todos los derechos reservados 2021'], style={'font-size':'14px','color': '#99abb4'}),
                                    ], style={'line-height':'25px','width':'60%'}
                                    ),

                            html.Div([
                                    html.P([html.A('Términos y condiciones', href='https://ourworldindata.org/', target='_blank'), 
                                            html.A('Política de privacidad', href='http://www.fao.org/faostat/en/#data', target='_blank',style={'padding-left':'15px'}),
                                            html.A('Aviso Legal', href='http://www.fao.org/faostat/en/#data', target='_blank',style={'padding-left':'15px'}),
                                            ], style={'font-size':'14px'}, className='pie_pagina')
                                    ], style={'line-height':'25px','width':'40%'}
                                    ),
                        ], className = 'footer', style={'background-color': '#282b38'}
                        ),
                    ],className='fila'
                    )
                ],className='contenedor'
                ), 
    
    ],style={'background':'#282b38'}

)


@app.callback(Output('url_login', 'pathname'),
              [Input('btn4', 'n_clicks'),
              Input('input_email', 'n_submit'),
               Input('input_password', 'n_submit')],
              [State('input_email', 'value'),
               State('input_password', 'value')])
def sucess(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):
    user = User.query.filter_by(email=input1).first()    # hace una consulta en la columna username para saber si se encuentra el email escrito en el login
    
    if user!=None:
        if check_password_hash(user.password, input2):  # se verifica la contraseña, comprueba si el hash del parámetro password coincide con el del usuario
            print(f'\nBienvenido {user.email}\n')
            login_user(user)    # inicia la sesión de un usuario 
           
            return '/dashboard'
        else:
            pass
    else:
        pass
         

@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:   # la instancia current_user contiene el valor del callback de user_loader y comprueba si el usuario actual ya está autenticado
        return html.Div('Usuario: ' + current_user.username)
        
    else:
        return ''


@app.callback(Output('output-state', 'children'),
              [Input('btn4', 'n_clicks'),
               Input('input_email', 'n_submit'),
               Input('input_password', 'n_submit')],
              [State('input_email', 'value'),
               State('input_password', 'value')])
def update_output(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):
    if n_clicks > 0 or n_submit_uname > 0 or n_submit_pwd > 0:
        user = User.query.filter_by(email=input1).first()
        if user:
            if check_password_hash(user.password, input2):  # si existe el usuario, entonces va a comprobar la contraseña
                return ''
            else:
                return html.Div([html.Br(),html.Div('El usuario o la contraseña es incorrecta')], className='contenedor fila', style={'color':'red','margin-top':'20px'})
        else:
            return html.Div([html.Br(),html.Div('El usuario no existe o faltó un campo')], className='contenedor fila',style={'color':'red','margin-top':'20px'})
    else:
        return ''

#if __name__ == '__main__':
#    app.run_server(debug=True)
