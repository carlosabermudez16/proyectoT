from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from server import app
import dash_daq as daq
import os
import os.path
from os import path
app.config.suppress_callback_exceptions = True
#-----------------------------------------------------------------------------------

sel3 = html.Div([
            daq.ToggleSwitch(
                    id='selector3',
                    label=['TOTAL ESTUDIANTES', 'FALLAS ESTUDIANTES'],
                    #style={'width': '250px', 'margin': 'auto'},
                    value=False,
                    color = '#e55467',
                ),
            ],className='selector3 col-lg-8')

sel4 = html.Div([
            daq.ToggleSwitch(
                    id='selector4',
                    label=['GRUPO', 'DOCENTE'],
                    #style={'width': '250px', 'margin': 'auto'},
                    value=False,
                    color = 'rgb(255, 71, 38)',
                ),
            ],className='selector4 col-lg-4')

bar3 = html.Div([dcc.Graph(id='graph3',config = {
								"displayModeBar": False
							}),
                ],className = "grafica1 col-lg-8")

bar4 = html.Div([dcc.Graph(id='graph4',config = {
								"displayModeBar": False
							}),
                ],className = "grafica2 col-lg-4")

size = [600, 400, 600, 800, 100, 800, 600, 400, 200, 400]
figura5 = go.Figure(
    data = [
             go.Scatter(
                    x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y=[11, 12, 10, 11, 12, 11, 12, 13, 12, 11],
                    mode='markers+lines',
                    line = dict(
                                width = 1,
                                color = "MediumPurple"
                            ),
                    marker=dict(
                        size=[i for i in size],
                        sizemode='area',
                        #sizeref=2.*max(size)/(40.**2),
                        sizemin=4,
                        color = [11, 12, 10, 11, 12, 11, 12, 13, 12, 11],
                        colorscale="Viridis",
                        opacity=1,
                        line = dict(
                                    color = "MediumPurple",
                                    width = 2
                                ),
                        )
                ),
        ],
    layout = go.Layout(
                    title = {
                        "text": "SECUENCIA DE GRUPOS DE CLASE",
                        "y": 0.93,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top"
                    },
                    titlefont = {
                        "color": "#a5b1cd",
                        "size": 20
                    },
                    xaxis = {
                        "title": "<b>Cantidad de asignaturas</b>",
                        "color": "white",
                        "showline": True,
                        "showgrid": False,
                        "showticklabels": True,
                        "linecolor": "white",
                        "linewidth": 1,
                        "ticks": "outside",
                        "tickfont": {
                            "family": "Aerial",
                            "color": "white",
                            "size": 12
                        }
                    },
                    yaxis = {
                        "title": "<b>Cantidad de clases</b>",
                        "color": "white",
                        "showline": True,
                        "showgrid": False,
                        "showticklabels": True,
                        "linecolor": "white",
                        "linewidth": 1,
                        "ticks": "outside",
                        "tickfont": {
                            "family": "Aerial",
                            "color": "white",
                            "size": 12
                        }
                    },
                    font = {
                        "family": "sans-serif",
                        "color": "white",
                        "size": 12
                    },
                    hovermode = "closest",
                    paper_bgcolor = "#1f2c56",
                    plot_bgcolor = "#1f2c56",
                    legend = {
                        "orientation": "h",
                        "bgcolor": "#1f2c56",
                        "xanchor": "center",
                        #"x": 0.5,
                        #"y": -0.7
                    }
                )
    
    )
bar5 = html.Div([dcc.Graph(id='graph5',config = {
								"displayModeBar": False
							},
                            figure = figura5),
                ],className = "grafica1 col-lg-7")

theme = {
    'dark': False,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E'
}
fondo_color = html.Div([
    daq.ToggleSwitch(
        id='daq-light-dark-theme',
        label=['claro', 'oscuro'],
        color = '#2186f4',
        style={'padding':'3px','margin': '0', 'position':'fixed','bottom':'0','z-index':'2',
                'background-color': '#a5b1cd','border-radius':'5px'},
        value=True
    ),
], id='dark-theme-provider-demo',className = "col-lg-2")

@app.callback(
    Output('dark-theme-provider-demo', 'style'),
    Input('daq-light-dark-theme', 'value')
)
def change_bg(dark_theme):
    if(dark_theme):
        return {'background': '#141e3f', 'color': '#a5b1cd'}
    else:
        return {'background': '#f6f6fc', 'color': 'black'}
#-----------------------------------------------------------------------------------

layout = html.Div([
    fondo_color,
    
    sel3,
    bar3,
    sel4,
    bar4,

    bar5,
    
])

# -------------------------------------------------------------------------------------

@app.callback(Output('graph3', 'figure'),
              [Input('selector3', 'value'),
               Input(component_id='table', component_property="derived_virtual_data"),
               Input(component_id='table', component_property='derived_virtual_selected_rows'),
               Input(component_id='table', component_property='derived_virtual_selected_row_ids'),
               Input(component_id='table', component_property='selected_rows'),
               Input(component_id='table', component_property='derived_virtual_indices'),
               Input(component_id='table', component_property='derived_virtual_row_ids'),
               Input(component_id='table', component_property='active_cell'),
               Input(component_id='table', component_property='selected_cells'),
               ])
def update_graph(selector3, all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    print('*'*20)
    print(selector3)
    print(all_rows_data)
    print(slctd_row_indices)
    print(order_of_rows_indices)
    print('*'*20)
    
    dffa = pd.DataFrame(all_rows_data)
    
    colors = ['#F65114' if i in slctd_row_indices else '#00d970' for i in range(len(dffa))]
    colors2 = ['#6713F0' if i in slctd_row_indices else '#e55467' for i in range(len(dffa))]
    
    g = os.listdir(f"./Data_base_firebase2/DOCENTES/107435720803934230443/107435720803934230443_Yolfanis Vides Uribe_FORMACION PEDAGOGICA .FR001/FOTO_CLASE")
    var = "data1/asistencia_cm.csv"

    if path.exists(var):
        df2 = pd.read_csv(var)
        dfa = pd.read_csv('./data1/Asistencia.csv')
        

        if (dffa.empty or len(dffa.columns) < 1):
            return {
                'data': [{
                    'x': [],
                    'y': [],
                    'type': 'bar'
                }]
            }
        elif selector3 == False:
            fig =  {
                    "data": [
                        
                        go.Bar(
                            x = df2["Nombre"],
                            y = df2["Total_As"],
                            texttemplate =  "%{y:,.0f}",
                            textposition = "auto",
                            marker = dict(
                                        color = colors
                                    ),
                            hoverinfo = "text",
                            hovertemplate =
                            "<b>Nombre</b>: %{x} <br>" +
                            "<b>Asistencia</b>:  %{y:,.0f} <br>" +
                            "<b>Clases</b>: " + str(len(g)) + "<br>"+"<extra></extra>"
                        ),
                    ],
                    "layout": go.Layout(
                        title = {
                            "text": "TOTAL ESTUDIANTES",
                            "y": 0.83,
                            "x": 0.5,
                            "xanchor": "center",
                            "yanchor": "top"
                        },
                        titlefont = {
                            "color": "#a5b1cd",
                            "size": 20
                        },
                        xaxis = {
                            'categoryorder': 'total ascending',
                            "title": "<b>Nombre Estudiantes</b>",
                            "color": "white",
                            "showline": True,
                            "showgrid": True,
                            "showticklabels": True,
                            "linecolor": "white",
                            "linewidth": 1,
                            "ticks": "outside",
                            "tickfont": {
                                "family": "Aerial",
                                "color": "white",
                                "size": 12
                            }
                        },
                        yaxis = {
                            "title": "<b>Asistencia</b>",
                            "color": "white",
                            "showline": True,
                            "showgrid": True,
                            "showticklabels": True,
                            "linecolor": "white",
                            "linewidth": 1,
                            "ticks": "outside",
                            "tickfont": {
                                "family": "Aerial",
                                "color": "white",
                                "size": 12
                            }
                        },
                        font = {
                            "family": "sans-serif",
                            "color": "white",
                            "size": 12
                        },
                        hovermode = "closest",
                        paper_bgcolor = "#1f2c56",
                        plot_bgcolor = "#1f2c56",
                        legend = {
                            "orientation": "h",
                            "bgcolor": "#1f2c56",
                            "xanchor": "center",
                            #"x": 0.5,
                            #"y": -0.7
                        }
                    )
                }
            
            return fig
        
        elif selector3 == True:
            fig =  {
                    "data": [
                        
                        go.Bar(
                            x = df2["Nombre"],
                            y = df2["Fallas"],
                            texttemplate =  "%{y:,.0f}",
                            textposition = "auto",
                            marker = dict(
                                        color = colors2
                                    ),
                            hoverinfo = "text",
                            hovertemplate =
                            "<b>Nombre</b>: %{x} <br>" +
                            "<b>Inasistencia</b>:  %{y:,.0f} <br>" +
                            "<b>Clases</b>: " + str(len(g)) + "<br>"+"<extra></extra>"
                        ),
                    ],
                    "layout": go.Layout(
                        title = {
                            "text": "FALLAS ESTUDIANTES",
                            "y": 0.83,
                            "x": 0.5,
                            "xanchor": "center",
                            "yanchor": "top"
                        },
                        titlefont = {
                            "color": "#a5b1cd",
                            "size": 20
                        },
                        xaxis = {
                            'categoryorder': 'total ascending',
                            "title": "<b>Nombre Estudiantes</b>",
                            "color": "white",
                            "showline": True,
                            "showgrid": True,
                            "showticklabels": True,
                            "linecolor": "white",
                            "linewidth": 1,
                            "ticks": "outside",
                            "tickfont": {
                                "family": "Aerial",
                                "color": "white",
                                "size": 12
                            }
                        },
                        yaxis = {
                            "title": "<b>Fallas</b>",
                            "color": "white",
                            "showline": True,
                            "showgrid": True,
                            "showticklabels": True,
                            "linecolor": "white",
                            "linewidth": 1,
                            "ticks": "outside",
                            "tickfont": {
                                "family": "Aerial",
                                "color": "white",
                                "size": 12
                            }
                        },
                        font = {
                            "family": "sans-serif",
                            "color": "white",
                            "size": 12
                        },
                        hovermode = "closest",
                        paper_bgcolor = "#1f2c56",
                        plot_bgcolor = "#1f2c56",
                        legend = {
                            "orientation": "h",
                            "bgcolor": "#1f2c56",
                            "xanchor": "center",
                            #"x": 0.5,
                            #"y": -0.7
                        }
                    )
                }
            
            return fig
    else:
        if (dffa.empty or len(dffa.columns) < 1):
            return {
                'data': [{
                    'x': [],
                    'y': [],
                    'type': 'bar'
                }]
            }

@app.callback(Output('graph4', 'figure'),
              [Input('selector4', 'value'),
               Input(component_id='table', component_property="derived_virtual_data"),
               Input(component_id='table', component_property='derived_virtual_selected_rows'),
               Input(component_id='table', component_property='derived_virtual_selected_row_ids'),
               Input(component_id='table', component_property='selected_rows'),
               Input(component_id='table', component_property='derived_virtual_indices'),
               Input(component_id='table', component_property='derived_virtual_row_ids'),
               Input(component_id='table', component_property='active_cell'),
               Input(component_id='table', component_property='selected_cells'),
               ])
def update_graph(selector4, all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    
    dffa = pd.DataFrame(all_rows_data)
    colors = ['#F65114' if i in slctd_row_indices else '#00d970'
              for i in range(len(dffa))]
    colors2 = ['#6713F0' if i in slctd_row_indices else '#F01313'
              for i in range(len(dffa))]
    g = os.listdir(f"./Data_base_firebase2/DOCENTES/107435720803934230443/107435720803934230443_Yolfanis Vides Uribe_FORMACION PEDAGOGICA .FR001/FOTO_CLASE")
    var1 = "data1/Asistencia.csv"
    if path.exists(var1):
        
        dfa = pd.read_csv(var1)

        list_chosen_countries=dfa['Nombre estudiante'].tolist()
        list_chosen_clase=dfa['dateRep'].tolist()
        columna_1 = []
        columna_2 = []
        columna_3 = []
        columna_4 = []
        columna_5 = []

        for i in list_chosen_countries:
            if i not in columna_1:
                cantidad = list_chosen_countries.count(i)
                columna_1.append(i)
                columna_2.append(cantidad)
            else:
                columna_1.append(None)
                columna_2.append(None)
        for i in list_chosen_clase:
            columna_5.append(64)
            if i not in columna_3:
                cantidad = list_chosen_clase.count(i)
                columna_3.append(i)
                columna_4.append(2)
            else:
                columna_3.append(None)
                columna_4.append(0)

        dfa['Total_Es'] = columna_1
        dfa['Total_As'] = columna_2
        dfa['Fechas clase'] = columna_3
        dfa['Horas realizadas'] = columna_4
        dfa['Horas semestre'] = columna_5

        horas_clase = 2
        clases_f = len(g)
        horas_realizadas = horas_clase*clases_f

        if (dffa.empty or len(dffa.columns) < 1):
            return {
                'data': [{
                    'x': [],
                    'y': [],
                    'type': 'bar'
                }]
            }
        elif selector4 == False:
            fig = {
                "data": [
                    go.Pie(
                        labels = ['Horas realizadas','Horas semestre faltante'],
                        values = [horas_realizadas, dfa['Horas semestre'][0] - horas_realizadas],
                        marker = {
                            "colors": ['rgb(42, 250, 219)','rgb(65,105,225)'],
                        },
                        hoverinfo = "label+value+percent",
                        textinfo = "label+value",
                        hole = 0.7,
                        rotation = 45,
                        insidetextorientation = "radial"
                    )
                ],
                "layout": go.Layout(
                    title = {
                        "text": "GRUPO",
                        "y": 0.83,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top"
                    },
                    titlefont = {
                        "color": "#a5b1cd",
                        "size": 20
                    },
                    font = {
                        "family": "sans-serif",
                        "color": "white",
                        "size": 10
                    },
                    hovermode = "closest",
                    paper_bgcolor = "#1f2c56",
                    plot_bgcolor = "#1f2c56",
                    legend = {
                        "orientation": "h",
                        "bgcolor": "#1f2c56",
                        "xanchor": "center",
                        "x": 0.5,
                        #"y": -0.5
                    }
                )
                }
            return fig
        
        elif selector4 == True:
            fig = {
                "data": [
                    go.Pie(
                        labels = ['Horas realizadas','Horas semestre faltante'],
                        values = [horas_realizadas, dfa['Horas semestre'][0] - horas_realizadas],
                        marker = {
                            "colors": ['rgb(90, 242, 168)','rgb(255, 71, 38)'],
                        },
                        hoverinfo = "label+value+percent",
                        textinfo = "label+value",
                        hole = 0.7,
                        rotation = 45,
                        insidetextorientation = "radial"
                    )
                ],
                "layout": go.Layout(
                    title = {
                        "text": "AÚN NO SÉ",
                        "y": 0.83,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top"
                    },
                    titlefont = {
                        "color": "#a5b1cd",
                        "size": 20
                    },
                    font = {
                        "family": "sans-serif",
                        "color": "white",
                        "size": 10
                    },
                    hovermode = "closest",
                    paper_bgcolor = "#1f2c56",
                    plot_bgcolor = "#1f2c56",
                    legend = {
                        "orientation": "h",
                        "bgcolor": "#1f2c56",
                        "xanchor": "center",
                        "x": 0.5,
                        #"y": -0.7
                    }
                )
                }
            return fig
    else:
        if (dffa.empty or len(dffa.columns) < 1):
            return {
                'data': [{
                    'x': [],
                    'y': [],
                    'type': 'bar'
                }]
            }


#if __name__ == '__main__':
#    app.run_server(debug=True)

    
