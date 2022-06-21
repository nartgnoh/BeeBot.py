# *********************************************************************************************************************
# music.py
# import cogs.helper.helper_functions.music as music_helper
# *********************************************************************************************************************

import os
import discord
import json
import urllib
import urllib.request
import subprocess
import youtube_dl

from youtube_search import YoutubeSearch

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
ytlinks_json = "/".join(list(current_directory.split('/')
                             [0:-3])) + '/resource_files/music_files/yt_links.json'


# # get ytlinks_json first element
def get_current_song():
    with open(ytlinks_json) as f:
        return json.load(f)[0]


# get ytlinks_json second element
def get_next_song():
    with open(ytlinks_json) as f:
        return json.load(f)[1]


# get ytlinks_json entire list
def all_songs_list():
    with open(ytlinks_json) as f:
        return json.load(f)


# if "url" is not a real url link, then "YoutubeSearch" and create new a YouTube url link
def add_url(yt_search_or_link):
    new_yt = YoutubeSearch(yt_search_or_link, max_results=1).to_json()
    yt_links_json = all_songs_list()
    data = yt_links_json + [json.loads(new_yt)["videos"][0]]
    with open(ytlinks_json, 'w') as outfile:
        json.dump(data, outfile)


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
        if file.endswith(".mp3"):
            os.rename(file, "resource_files/music_files/song.mp3")


# download next_song.mp3
def download_next_song():
    next_song = get_next_song()
    youtube_url = "https://www.youtube.com/" + next_song["url_suffix"]
    # download audio into "next_song.mp3"
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
    # move .mp3 file to next_song.mp3
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "resource_files/music_files/next_song.mp3")
