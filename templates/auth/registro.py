from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from server import app

# Create app layout
layout = html.Div(children=[
    dcc.Location(id='url_register', refresh=True),
    
    html.Div([
            html.Div([
                    html.Div(id='fondo1'),
                    html.Div(id='fondo2'),
                    html.Div(id='fondo3'),
                    html.Div(id='fondo4'),
                    ],className='fila')
            ],className='contenedor'),
    html.Div(style={'margin-top':'10%'}),            
    html.Div([
                html.Div([
                    html.Div([
                        html.Div([ html.H1('_')],className='col-lg-4 col-md-4 col-sm-4',style={'color':'rgba(255,255,255,0)',
                                        'background':'transparent'}),
                        html.Div([    
                            dcc.Input(
                                placeholder='Nombre de usuario',
                                n_submit=0,
                                type='text',
                                id='input_username'
                            ),
                            
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
                            html.Br(), html.Br(),
                            html.Button(
                                children='Continue',
                                n_clicks=0,
                                type='submit',
                                id='btn5'
                            ),
                        ],className='col-lg-4',id='orden1',style={'text-align': 'center'}),   
                        html.Div([ html.H1('_')],className='col-lg-4 col-md-4 col-sm-4',style={'color':'rgba(255,255,255,0)',
                                        'background':'transparent'}),
                        html.Div(children='', id='output-state2')
                    ],className='col-lg-12'),  
                    ], className="fila", )
        ], className="contenedor", )
])




@app.callback(Output('url_register', 'pathname'),
              [Input('btn5', 'n_clicks'),
              Input('input_username', 'n_submit'),
              Input('input_email', 'n_submit'),
               Input('input_password', 'n_submit'),
               ],
              [ State('input_username', 'value'),
                State('input_email', 'value'),
                State('input_password', 'value'),])
def cargando(n_clicks, n_submit_usuario,n_submit_email, n_submit_pwd, input1, input2,input3):
    
    
    if n_clicks != 0 and input1!=None and input2!=None and input3!=None:
        
        from controller.database_work import insert_user
        insert_user(username=input1,email=input2,password=input3)
        
        print('\nRegistro de datos exitosos!')
        
        return '/login'
    else:
        return '/registro'


