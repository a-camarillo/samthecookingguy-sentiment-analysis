import os

import googleapiclient.discovery
import json

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ['GOOGLE_API']

#create youtube api object
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

def get_video_details(id_list):
    '''This function gets video details from Video API endpoint'''

    results = youtube.videos().list(
        part = 'snippet',
        id = id_list
    ).execute()
    return results

def store_video_details(videos):
    '''This function extracts data from Video response'''
    for item in videos['items']:
        video_ids.append(item['id'])
        video_title.append(item['snippet']['title'])
        published_at.append(item['snippet']['publishedAt'])

video_ids = []
video_title = []
published_at = []
data_dict = {}

videos = get_video_details(['5h974fXFFHE','4tc4L85OyWQ','R5MDtcS1VAU'])
store_video_details(videos)

data_dict.update({'video_id':video_ids})
data_dict.update({'video_title':video_title})
data_dict.update({'published':published_at})
print(data_dict)
