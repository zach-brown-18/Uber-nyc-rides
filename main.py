import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np


# April-September 2014
df_april = pd.read_csv('df_april.csv', index_col=0)
df_may = pd.read_csv('df_may.csv', index_col=0)
df_june = pd.read_csv('df_june.csv', index_col=0)
df_july = pd.read_csv('df_july.csv', index_col=0)
df_august = pd.read_csv('df_august.csv', index_col=0)
df_september = pd.read_csv('df_september.csv', index_col=0)

frames = [df_april, df_may, df_june, df_july, df_august, df_september]

# Filtering functions
# Takes string date in form #/##/####
def ridesOnDay(DATE, DF_MONTH):
    return DF_MONTH[DF_MONTH['Date/Time'].str.match(DATE)]

# Works for current state. Would be updated if the program receives more data
def findDF(MONTH, YEAR):
    return frames[int(MONTH)-4] if YEAR == "2014" else None

def hour(DF, HOUR):
    return DF[DF["Hour"] == int(HOUR)]

def splitYearMonthDay(date):
    date = date.replace('T', ' ')
    date = date.split(' ')[0].split('-')
    return date

def extractMonth(date):
    date = splitYearMonthDay(date)
    return date[1]

def extractYear(date):
    date = splitYearMonthDay(date)
    return date[0]

def formatDateString(date):
    date = splitYearMonthDay(date)
    date_string = date[1].lstrip('0') + '/' + date[2].lstrip('0') + '/' + date[0]
    return date_string

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
                dcc.Dropdown(id='hour_input',
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
        df = findDF(extractMonth(date), extractYear(date))
        date_string = formatDateString(date)
        result = ridesOnDay(date_string, df)
        
        counts, bins = np.histogram(result["Hour"], bins=range(1, 26))
        bins = range(1, 25)

        fig_hist = px.bar(
            x=bins,
            y=counts,
            color=bins,
            text=counts,
            color_discrete_sequence=colors,
        )

        fig_hist.update_traces(
            textposition='outside',
            hovertemplate='Hour: %{x}<br>' + 'Rides: %{y}'
        )
        fig_hist.layout.update(
            showlegend=False,
            dragmode='select',
            plot_bgcolor='#696969',
            paper_bgcolor='#696969',
            margin={'l': 0, 'r': 0, 'b': 140, 't': 10},
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                title=None,
                fixedrange=True,
                visible=True,
                dtick=1
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                fixedrange=True,
                visible=False
            ))
        
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
    
    df = findDF(extractMonth(DATE), extractYear(DATE))
    date_string = formatDateString(DATE)
    result = ridesOnDay(date_string, df)
    
    if HOUR is not None:
        if HOUR:
            for selection in range(len(HOUR)):
                if selection==0:
                    temp_result = hour(result, HOUR[selection])
                else:
                    temp_result = temp_result.append(hour(result, HOUR[selection]))
            
            result = temp_result

    fig_scat = px.scatter_mapbox(
        result,
        lat="Lat",
        lon="Lon",
        color="Hour",
    )
    
    fig_scat.layout.update(
        autosize=True,
        paper_bgcolor='#696969',
        mapbox=dict(
            accesstoken=mapbox_token,
            center=dict(
                lat=40.7189,
                lon=-73.9506
            ),
        zoom=11
        ),
        margin={'l':0, 'r':0, 'b':0, 't':0}
    )
    
    counts = len(result.index)
    str_output = str(counts) + " rides"
    
    return fig_scat, str_output

if __name__ == '__main__':
    app.run_server(debug=True)