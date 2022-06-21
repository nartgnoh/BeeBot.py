# *********************************************************************************************************************
# music.py
# import cogs.helper.helper_functions.music as music_helper
# *********************************************************************************************************************

import os
import json
import youtube_dl

from datetime import datetime
from youtube_search import YoutubeSearch

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
ytlinks_json = "/".join(list(current_directory.split('/')
                             [0:-3])) + '/resource_files/music_files/yt_links.json'
song_mp3_path = "/".join(list(current_directory.split('/')
                              [0:-3])) + '/resource_files/music_files/song.mp3'


# check if ytlinks_json is empty
def check_current_song():
    with open(ytlinks_json) as f:
        if json.load(f)[0]:
            return True
        else:
            return False


# check if ytlinks_json is empty without the first element (current)
def check_rest_songs_list():
    with open(ytlinks_json) as f:
        if json.load(f)[1:]:
            return True
        else:
            return False


# check duration of song is under 15mins
def check_duration(yt_json):
    duration = datetime.strptime(yt_json['duration'], '%M:%S')
    # if yt_json[]


# get ytlinks_json first element
def get_current_song():
    with open(ytlinks_json) as f:
        return json.load(f)[0]


# get ytlinks_json second element
def get_next_song():
    with open(ytlinks_json) as f:
        return json.load(f)[1]


# get ytlinks_json entire list
def get_songs_list():
    with open(ytlinks_json) as f:
        return json.load(f)


def reset_songs_list():
    with open(ytlinks_json, 'w') as outfile:
        json.dump([], outfile)


# if "url" is not a real url link, then "YoutubeSearch" and create new a YouTube url link
def add_url(yt_search_or_link):
    yt_search = YoutubeSearch(yt_search_or_link, max_results=1).to_json()
    new_yt_json = json.loads(yt_search)["videos"][0]
    yt_links_json = get_songs_list()
    data = yt_links_json + [new_yt_json]
    with open(ytlinks_json, 'w') as outfile:
        json.dump(data, outfile)
    return new_yt_json


# delete first url from ytlinks_txt
def delete_first_song():
    with open(ytlinks_json, 'r') as f:
        data = json.load(f)
    with open(ytlinks_json, 'w') as outfile:
        json.dump(data[1:], outfile)


# download song.mp3
def download_song():
    current_song = get_current_song()
    youtube_url = "https://www.youtube.com/" + current_song["url_suffix"]
    # download audio into "song.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    # download .mp3
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    # move .mp3 file to song.mp3
    for file in os.listdir("./"):
        if file.endswith(".mp3") or file.endswith(".webm"):
            os.rename(file, song_mp3_path)


# go next
def download_next_song():
    delete_first_song()
    download_song()
