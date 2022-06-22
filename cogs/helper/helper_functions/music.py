# *********************************************************************************************************************
# music.py
# import cogs.helper.helper_functions.music as music_helper
# *********************************************************************************************************************

import os
import discord
import json
import youtube_dl

from datetime import datetime
from youtube_search import YoutubeSearch

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
songs_list_json = "/".join(list(current_directory.split('/')
                                [0:-3])) + '/resource_files/music_files/songs_list.json'
music_files_directory = "/".join(list(current_directory.split('/')
                                      [0:-3])) + '/resource_files/music_files/'

# song_mp3_path = "/".join(list(current_directory.split('/')
#                               [0:-3])) + '/resource_files/music_files/song.mp3'
# song2_mp3_path = "/".join(list(current_directory.split('/')
#                                [0:-3])) + '/resource_files/music_files/song2.mp3'


# get songs_list_json entire list
def get_songs_list():
    with open(songs_list_json) as f:
        return json.load(f)


# get songs_list_json first element
def get_current_song():
    return get_songs_list()[0]


# get songs_list_json second element
def get_next_song():
    return get_songs_list()[1]


# reset songs list
def reset_songs_list():
    with open(songs_list_json, 'w') as outfile:
        json.dump([], outfile)


# delete first url from ytlinks_txt
def delete_first_song():
    with open(songs_list_json, 'r') as f:
        data = json.load(f)
    with open(songs_list_json, 'w') as outfile:
        json.dump(data[1:], outfile)


# if "url" is not a real url link, then "YoutubeSearch" and create new a YouTube url link
def add_url(yt_search_or_link):
    yt_search = YoutubeSearch(yt_search_or_link, max_results=1).to_json()
    new_yt_json = json.loads(yt_search)["videos"][0]
    yt_links_json = get_songs_list()
    data = yt_links_json + [new_yt_json]
    with open(songs_list_json, 'w') as outfile:
        json.dump(data, outfile)


# download song using youtube_dl
def download_song(song, path):
    print("~~~~~~~~~ Downloading Music ~~~~~~~~~")
    youtube_url = "https://www.youtube.com/" + song["url_suffix"]
    ydl_opts = {'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, path)


# play songs
def play_songs(ctx):
    song_mp3_path = music_files_directory + 'song.mp3'
    song2_mp3_path = music_files_directory + 'song2.mp3'
    # remove "song.mp3" file
    try:
        if os.path.isfile(song_mp3_path):
            os.remove(music_files_directory + 'song.mp3')
    except PermissionError:
        print('~~~~~~~~~ Error in play_songs() at FIRST try/except ~~~~~~~~~ ')
    try:
        # rename "song2.mp3" to "song.mp3" if song2.mp3 exists
        if os.path.isfile(song2_mp3_path):
            os.rename(song2_mp3_path, song_mp3_path)
    except PermissionError:
        print('~~~~~~~~~ Error in play_songs() at SECOND try/except ~~~~~~~~~ ')

    # playing songs
    songs_list = get_songs_list()
    if len(songs_list) > 0:

        
        # if len(songs_list) > 1 and os.path.isfile(song_mp3_path):
        #     print('~~~~~~~~~ Downloading 2 songs ~~~~~~~~~ ')
        #     download_song(get_current_song(), song_mp3_path)

        #     download_song(get_next_song(), song2_mp3_path)

        # else:
        #     download_song(get_current_song())
        # play ffmpeg
        voice = ctx.voice_client
        voice.play(discord.FFmpegPCMAudio(song_mp3_path),
                   after=lambda e: play_next(ctx))
        voice.is_playing()
    else:
        voice.disconnect()
        reset_songs_list()
        print("~~~~~~~~~ No more audio in queue ~~~~~~~~~")


# play next song
def play_next(ctx):
    print("~~~~~~~~~ Inside play_next ~~~~~~~~~")
    delete_first_song()
    play_songs(ctx)
