import json 
import pandas as pd 
import datetime
import pyodbc

with open('json_data/video_info.json','r') as f:
    data = json.load(f)

df = pd.DataFrame({key:pd.Series(value) for key,value in data.items()})
df['published'] = pd.to_datetime(df['published'])
df['published_year'] = df['published'].dt.year
df['published_month'] = df['published'].dt.month
df['published_day'] = df['published'].dt.day
df['published_time'] = df['published'].dt.time

server = 'DESKTOP-H5MDRS4\SQLEXPRESS'
database = 'youtube_db'

#connect to MS SQL SERVER
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                      SERVER=' + server + ';  \
                      DATABASE=' + database +'; \
                      Trusted_Connection=yes;')

cursor = cnxn.cursor()

insert_query = '''
                INSERT INTO VideoDetails (videoID,videoTitle,uploadDatetime,uploadYear,uploadMonth,uploadDay,uploadTime)
                VALUES (?,?,?,?,?,?,?);
               '''

for column, value in df.iterrows():
    row = list(value)
    cursor.execute(insert_query, row)

#commit query
cnxn.commit()

#close connection
cursor.close()
cnxn.close()


