import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

# # Load data on rides
# # April-September 2014
# df_april = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-apr14.csv')
# df_may = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-may14.csv')
# df_june = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-jun14.csv')
# df_july = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-jul14.csv')
# df_august = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-aug14.csv')
# df_september = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-sep14.csv')

# # Add 'Hour' bin
# def toHour(dateTimeStr:str)->str:
#     return int(dateTimeStr.split(" ")[1].split(":")[0]) + 1

# frames = [df_april, df_may, df_june, df_july, df_august, df_september]

# for month in frames:  
#     month["Hour"] = month["Date/Time"].apply(toHour)

# Load data on rides
# April-September 2014
df_april = pd.read_csv('df_april.csv')
df_may = pd.read_csv('df_may.csv')
df_june = pd.read_csv('df_june.csv')
df_july = pd.read_csv('df_july.csv')
df_august = pd.read_csv('df_august.csv')
df_september = pd.read_csv('df_september.csv')

frames = [df_april, df_may, df_june, df_july, df_august, df_september]

# Filtering functions
# Takes (string date in form ##/##/####, dataframe to be selected from)
def ridesOnDay(DATE, DF_MONTH):
    return DF_MONTH[DF_MONTH['Date/Time'].str.match(DATE)]

# Works for current state. Would be updated if the program receives more data
# Takes (string or int month, string year)
def findDF(MONTH, YEAR):
    return frames[int(MONTH)-4] if YEAR == "2014" else None

# Takes (dataframe of rides, integer hour filter)
def hour(DF, HOUR):
    return DF[DF["Hour"] == int(HOUR)]


# GUI

external_stylesheets = ['https://codepen.io/zach181818/pen/LYVoJrG.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background1': '#111111',
    'background2': '#008080',
    'text': '#7FDBFF'
}

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
                    date=dt(2014, 4, 15)
                ),

                html.Label('Hour'),
                dcc.Dropdown(id='hour_input',
                    options=[
                        {'label':'1', 'value':1},
                        {'label':'2', 'value':2},
                        {'label':'3', 'value':3},
                        {'label':'4', 'value':4},
                        {'label':'5', 'value':5},
                        {'label':'6', 'value':6},
                        {'label':'7', 'value':7},
                        {'label':'8', 'value':8},
                        {'label':'9', 'value':9},
                        {'label':'10', 'value':10},
                        {'label':'11', 'value':11},
                        {'label':'12', 'value':12},
                        {'label':'13', 'value':13},
                        {'label':'14', 'value':14},
                        {'label':'15', 'value':15},
                        {'label':'16', 'value':16},
                        {'label':'17', 'value':17},
                        {'label':'18', 'value':18},
                        {'label':'19', 'value':19},
                        {'label':'20', 'value':20},
                        {'label':'21', 'value':21},
                        {'label':'22', 'value':22},
                        {'label':'23', 'value':23},
                        {'label':'24', 'value':24}
                    ],
                    multi=True,
                ),

                html.Div(id='count_output')
                
                ])
            
            ],
            style={
                'fontFamily': 'Helvetica Neue'
            },
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
                style={
                    'height': '50vh'
                }
            ),

            html.Div(
                id='histogram_div',
                children=[
                    dcc.Graph(
                    id='histogram',
                    )
                ],
                style={
                    'height': '50vh'
                }
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
        # Extract date in format #/##/#### from date selector
        date = date.replace('T', ' ')
        date = date.split(' ')[0].split('-')

        date_string = date[1].lstrip('0') + '/' + date[2].lstrip('0') + '/' + date[0]
        df = findDF(date[1].lstrip('0'), date[0])
        result = ridesOnDay(date_string, df)
        
        # Build histogram
        counts, bins = np.histogram(result["Hour"], bins=range(1, 26))
        bins = range(1, 25)

        fig_hist = px.bar(
            x=bins,
            y=counts,
            color=bins,
            text=counts,
            color_discrete_sequence=colors,
        )

        # Formatting
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
    
    # Extract date in format #/##/#### from date selector
    DATE = DATE.replace('T', ' ')
    DATE = DATE.split(' ')[0].split('-')

    date_string = DATE[1].lstrip('0') + '/' + DATE[2].lstrip('0') + '/' + DATE[0]
    df = findDF(DATE[1].lstrip('0'), DATE[0])
    result = ridesOnDay(date_string, df)
    
    # Handle hour selection
    if HOUR is not None:
        if HOUR:
            for selection in range(len(HOUR)):
                if selection==0:
                    temp_result = hour(result, HOUR[selection])
                else:
                    temp_result = temp_result.append(hour(result, HOUR[selection]))
            
            result = temp_result

    # Plot scatter
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
    
    # update_counts section
    counts = len(result.index)
    str_output = str(counts) + " rides"
    
    return fig_scat, str_output

if __name__ == '__main__':
    app.run_server(debug=True)