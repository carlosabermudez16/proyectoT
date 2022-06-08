from server import app
from dash.dependencies import Input, Output
from dash import dcc
from dash import html



perfil = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([ html.A(' ')]), #html.Img(src='static/icon/user_profile.png',style={'width':'50px','height':'50px','margin':'-1px'}))]),
        style={
            'width': '50px',
            'height': '50px',
            'lineHeight': '60px',
            'borderColor': 'white',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '100%',
            'textAlign': 'center',
            'margin': '10px',
            'z-index':'3',
            'cursor':'pointer',
            #'background':'linear-gradient(-135deg, #2941b6, #f1eff1,#2941b6)',
            },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])


def parse_contents(contents):
    return html.Div([
            html.Img(
                src=contents,
                style={
                    'width': '50px',
                    'height': '50px',
                    'lineHeight': '60px',
                    #'borderWidth': '1px',
                    #'borderStyle': 'dashed',
                    'borderRadius': '100%',
                    #'margin': '10px',
                    'position':'absolute',
                    'top':'30px',
                    'right':'68px',
                    'z-index':'-1',
                    'cursor':'pointer',
                    },
                ),
        ],
        )


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),)
def update_output(list_of_contents):
    if list_of_contents is not None:
        children = [
            parse_contents(c) for c in list_of_contents]
        return children
