from __future__ import unicode_literals
from googleapiclient.discovery import build

import json
import youtube_dl
import os

CONFIG_FILE = 'config.json'
with open(CONFIG_FILE) as f:
    read_data = f.read()
config = json.loads(read_data)

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
API_KEY = config.get('api-key')
PLAYLIST_ID = config.get('playlist-id')
ALREADY_DLED = 'ids.json'

DEBUG = 0
if DEBUG:
    print("DEBUG FLAG is on")

def build_youtube_url(vid_id):
    return 'https://www.youtube.com/watch?v=' + vid_id

def get_playlist(service):
    response = service.playlistItems().list(
        part='snippet',
        maxResults=25,
        playlistId=PLAYLIST_ID
    ).execute()

    playlist = []
    for pl_item in response['items']:
        playlist.append(pl_item['snippet']['resourceId']['videoId'])

    # more items than maxResults
    while 'nextPageToken' in response:
        response = service.playlistItems().list(
            part='snippet',
            maxResults=25,
            pageToken=response['nextPageToken'],
            playlistId=PLAYLIST_ID
        ).execute()

        for pl_item in response['items']:
            playlist.append(pl_item['snippet']['resourceId']['videoId'])

    current_list = []
    if (os.path.isfile('./'+ALREADY_DLED)):
        with open(ALREADY_DLED) as f:
            read_data = f.read()
        current_list = json.loads(read_data)

    diff = set(playlist) - set(current_list)

    if DEBUG:
        print("Master\t    Local\n=======\t    =====")
        for i in range(len(playlist)):
            local_found = '----'
            if playlist[i] in current_list:
                local_found = playlist[i]
            print('{} {}'.format(playlist[i], local_found))

    with open(ALREADY_DLED, 'w+') as f:
        json.dump(playlist, f, indent=4)

    diff = [build_youtube_url(x) for x in diff]
    return diff

if __name__ == '__main__':
    service = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
    playlist = get_playlist(service)
    if not playlist:
        print('No new items added to playlist')
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': './music/%(title)s.%(ext)s',
        # 'simulate': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist)
    print('Finished')
