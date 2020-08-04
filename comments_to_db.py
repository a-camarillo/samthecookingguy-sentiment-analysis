import json 
import pandas as pd 
import datetime
import pyodbc

with open('pastrami_sandwich.json','r') as f:
    data = json.load(f)

df = pd.DataFrame({key:pd.Series(value) for key,value in data.items()})
df['video_Id'] = 'R5MDtcS1VAU'
df['comment_datetime'] = pd.to_datetime(df['comment_time'])
df['comment_year'] = df['comment_datetime'].dt.year
df['comment_month'] = df['comment_datetime'].dt.month
df['comment_day'] = df['comment_datetime'].dt.day
df['comment_time'] = df['comment_datetime'].dt.time

server = 'DESKTOP-H5MDRS4\SQLEXPRESS'
database = 'youtube_db'

#connect to MS SQL SERVER
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                      SERVER=' + server + ';  \
                      DATABASE=' + database +'; \
                      Trusted_Connection=yes;')

cursor = cnxn.cursor()

insert_query = '''
                INSERT INTO VideoComments (videoID,commentAuthor,userID,comment,commentTime,commentDateTime,commentYear,commentMonth,commentDay)
                VALUES (?,?,?,?,?,?,?,?,?);
               '''

for column, value in df.iterrows():
    row = list(value)
    cursor.execute(insert_query, row)

#commit query
cnxn.commit()

#close connection
cursor.close()
cnxn.close()
