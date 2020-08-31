import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
from helper_functions import ridesOnDay, findDF, findDFhour, extractMonth, extractYear, formatDateString
from helper_functions import setHistLayout, setScatLayout, updateHour, setRidesCount

# April-September 2014
months = ['april', 'may', 'june', 'july', 'august', 'september']
frames = [pd.read_csv(f'df_{month}.csv', index_col=0) for month in months]

# GUI

external_stylesheets = ['https://codepen.io/zach181818/pen/LYVoJrG.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background1': '#111111',
    'background2': '#008080',
    'text': '#7FDBFF'
}

hour_selection = [{'label':f'{n}', 'value':n} for n in range(1,25)]

app.layout = html.Div(id='all', children=[
    html.Div(
        id='split',
        children=[
        html.Div(id='left', children=[
            html.Div(id='title', children=[
                html.H1('NYC Uber Rides')],
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'backgroundColor': colors['background1']
                }
            ),
            
            html.Div(id='input', children=[
                html.Label('Date'),
                dcc.DatePickerSingle(
                    id='date_input',
                    min_date_allowed=dt(2014, 4, 1),
                    max_date_allowed=dt(2014, 9, 30),
                    date=dt(2014, 4, 15)
                ),

                html.Label('Hour'),
                dcc.Dropdown(
                    id='hour_input',
                    options=hour_selection,
                    multi=True,
                ),

                html.Div(id='count_output')
                
                ])
            
            ],
            style={'fontFamily': 'Helvetica Neue'},
            className = 'four columns'
        ),

        html.Div(id='right', children=[
            html.Div(
                id='scatter_div',
                children=[
                    dcc.Graph(
                        id='scatter',
                    )
                ],
                style={'height': '50vh'}
            ),

            html.Div(
                id='histogram_div',
                children=[
                    dcc.Graph(
                        id='histogram',
                    )
                ],
                style={'height': '50vh'}
            )],
        className = 'eight columns'
        )],
    
        style={
            'color': colors['text'],
            'backgroundColor': colors['background1']
        },
        className = 'row'
    )],
    
    style={
        'color': colors['text'],
        'backgroundColor': colors['background1'],
        'position':'fixed',
        'top':'0vh',
        'bottom':'0vh',
        'left':'0vw',
        'right':'0vw'
    },

    className='twelve columns'
)


@app.callback(
    Output('histogram', 'figure'),
    [Input('date_input', 'date')]
)
def update_histogram(date):
    if date is not None:
        df = findDF(frames, extractMonth(date), extractYear(date))
        date_string = formatDateString(date)
        result = ridesOnDay(date_string, df)
        
        counts, bins = np.histogram(result["Hour"], bins=range(1, 26))
        bins = range(1, 25)

        fig_hist = px.bar(
            x=bins,
            y=counts,
            color=bins,
            text=counts
        )
        fig_hist.update_traces(
            textposition='outside',
            hovertemplate='Hour: %{x}<br>' + 'Rides: %{y}'
        )
        setHistLayout(fig_hist)
        
        return fig_hist

@app.callback(
    [Output('scatter', 'figure'),
    Output('count_output', 'children')],
    [Input('hour_input', 'value'),
    Input('date_input', 'date')]
)

def update_scatter(HOUR, DATE):
    mapbox_token="pk.eyJ1IjoiemFjaDE4MTgxOCIsImEiOiJjazhrZjBkZHQwMTdxM2Zwem5obHBneDdtIn0.gG_MrTFb9TiejDTHKAdL2A"
    px.set_mapbox_access_token(mapbox_token)
    
    df = findDF(frames, extractMonth(DATE), extractYear(DATE))
    date_string = formatDateString(DATE)
    result = ridesOnDay(date_string, df)
    
    if HOUR:
        result = updateHour(result, HOUR)

    fig_scat = px.scatter_mapbox(
        result,
        lat="Lat",
        lon="Lon",
        color="Hour",
    )
    setScatLayout(fig_scat)
    
    str_output = setRidesCount(result)
    
    return fig_scat, str_output

if __name__ == '__main__':
    app.run_server(debug=True)