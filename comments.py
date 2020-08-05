import os

import googleapiclient.discovery
import json

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ['GOOGLE_API']
video_Id = 'bofQbiUPKXA'
#create the youtube api object
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def get_comment_threads(youtube,video_id,page_token=None):
    '''This function gets comment thread data from the Comment Thread API endpoint''' 
    results = youtube.commentThreads().list(
        part = "snippet",
        videoId = video_id,
        textFormat = 'plainText',
        maxResults = 100,
        pageToken = page_token
    ).execute()
    return results

def store_comments(comments):
    '''extract data from Comment Thread response'''
    for item in comments['items']:
        comment = item['snippet']['topLevelComment']
        author = comment_author.append(comment['snippet']['authorDisplayName'])
        text = comment_text.append(comment['snippet']['textDisplay'])
        time = comment_time.append(comment['snippet']['publishedAt'])
        id = comment_id.append(comment['snippet']['authorChannelId']['value'])
    
comment_author = []
comment_text = []
comment_time = []
comment_id = []

data_dict = {}


try:
    comments = get_comment_threads(youtube,video_id=video_Id)
    next_page_token = comments['nextPageToken']
    store_comments(comments)
    while next_page_token:
        comments = get_comment_threads(youtube,video_id=video_Id,page_token=next_page_token)
        next_page_token = comments['nextPageToken']
        store_comments(comments)
except KeyError:
    pass

data_dict.update({'video_Id':[f'{video_Id}']})
data_dict.update({'comment_author':comment_author})
data_dict.update({'user_id':comment_id})
data_dict.update({'comment_text':comment_text})
data_dict.update({'comment_time':comment_time})

with open('json_data/bourbon_chicken.json','w') as file:
    json.dump(data_dict, file)

