import pandas as pd
from csv import writer

# Load data on rides
# April-September 2014
df_april = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-apr14.csv')
df_may = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-may14.csv')
df_june = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-jun14.csv')
df_july = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-jul14.csv')
df_august = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-aug14.csv')
df_september = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-sep14.csv')

# Add 'Hour' bin
def to_hour(dateTimeStr:str)->str:
    return int(dateTimeStr.split(" ")[1].split(":")[0]) + 1

frames = [df_april, df_may, df_june, df_july, df_august, df_september]

for month in frames:  
    month["Hour"] = month["Date/Time"].apply(to_hour)

df_april = df_april[["Date/Time", "Lat", "Lon", "Hour"]]
df_may = df_may[["Date/Time", "Lat", "Lon", "Hour"]]
df_june = df_june[["Date/Time", "Lat", "Lon", "Hour"]]
df_july = df_july[["Date/Time", "Lat", "Lon", "Hour"]]
df_august = df_august[["Date/Time", "Lat", "Lon", "Hour"]]
df_september = df_september[["Date/Time", "Lat", "Lon", "Hour"]]

def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name+'.csv'

frames = [df_april, df_may, df_june, df_july, df_august, df_september]

for month in frames:
    month.to_csv(get_df_name(month))

df_july.to_csv('df_july.csv')