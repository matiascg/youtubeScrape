from _pytest.fixtures import scopes
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json
import io
import os
import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pathlib import Path

import google_auth_oauthlib.flow

import googleapiclient.errors

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

youTubeApiKey = 'AIzaSyBBJGRRF9QAj6AIjhRwL7ytof54lYk91oI'
youtube = build('youtube', 'v3', developerKey=youTubeApiKey)
channelId = 'UC-lHJZR3Gqxm24_Vd_AJ5Yw'

statdata = youtube.channels().list(part='statistics', id=channelId).execute()
stats = statdata['items'][0]['statistics']
print(stats)
print(statdata)

request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id="6yQ70Oid5zk"
    )
response = request.execute()

print(response)

request = youtube.captions().list(
    videoId="6yQ70Oid5zk",
    part="snippet"
)
response = request.execute()

print(response)

data_folder = Path("C:/Users/matia/youtubeScrape/Captions/caption")

id_n = "0qmufbVWtd001vLFPe7W8RYx2cISYA-5oRclPFVq7VA="
request = youtube.captions().download(
        id=id_n
    )
fh = io.FileIO(data_folder, "wb")

download = MediaIoBaseDownload(fh, request)
complete = False
while not complete:
    status, complete = download.next_chunk()

# function to download subtitles


def download_subs(url, lang="en"):
    opts = {
        "skip_download": True,
        "writesubtitles": "%(name)s.vtt",
        "subtitlelangs": lang,
        "writeautomaticsub": True
    }
    with youtube_dl.YoutubeDL(opts) as yt:
        yt.download([url])