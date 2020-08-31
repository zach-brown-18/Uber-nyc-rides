import plotly.express as px

# Takes string date in form #/##/####
def ridesOnDay(date, df_month):
    return df_month[df_month['Date/Time'].str.match(date)]

# Works for current state. Would be updated if the program receives more data
def findDF(frames, month, year):
    return frames[int(month)-4] if year == "2014" else None

def findDFhour(df, hour):
    return df[df["Hour"] == int(hour)]

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

def setHistLayout(fig):
    fig.layout.update(
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


def setScatLayout(fig):
    mapbox_token="pk.eyJ1IjoiemFjaDE4MTgxOCIsImEiOiJjazhrZjBkZHQwMTdxM2Zwem5obHBneDdtIn0.gG_MrTFb9TiejDTHKAdL2A"
    fig.layout.update(
    autosize=True,
    paper_bgcolor='#696969',
    mapbox=dict(
        accesstoken=mapbox_token,
        center=dict(lat=40.7189,lon=-73.9506),
        zoom=11
    ),
    margin={'l':0, 'r':0, 'b':0, 't':0})

def updateHour(df, hour):
    for selection in range(len(hour)):
        if selection==0:
            temp_result = findDFhour(df, hour[selection])
        temp_result = temp_result.append(findDFhour(df, hour[selection]))
    
    return temp_result

def setRidesCount(df):
    counts = len(df.index)
    str_output = str(counts) + " rides"
    return str_output