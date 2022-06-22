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
current_song_mp3_path = music_files_directory + 'song.mp3'
next_song_mp3_path = music_files_directory + 'next_song.mp3'


# *********************************************************************************************************************
# helper functions
# *********************************************************************************************************************
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


# check song duration under 15 mins
def check_song_duration(song_json):
    song_duration = song_json['duration'].split(':')
    # get song duration in seconds (mins*60 + secs)
    total_seconds = int(song_duration[-2]) * 60 + int(song_duration[-1])
    if total_seconds > 900:
        return False
    else:
        return True


# if "url" is not a real url link, then "YoutubeSearch" and create new a YouTube url link
def add_url(yt_search_or_link):
    yt_search = YoutubeSearch(yt_search_or_link, max_results=1).to_json()
    new_yt_json = json.loads(yt_search)["videos"][0]
    if check_song_duration(new_yt_json):
        yt_links_json = get_songs_list()
        data = yt_links_json + [new_yt_json]
        with open(songs_list_json, 'w') as outfile:
            json.dump(data, outfile)
        return new_yt_json
    else:
        return False


# *********************************************************************************************************************
# play music helper functions
# *********************************************************************************************************************
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


# play songs with ffmpeg
def play_song(ctx, path):
    voice = ctx.voice_client
    voice.play(discord.FFmpegPCMAudio(path),
               after=lambda e: play_next(ctx))
    voice.is_playing()


# *********************************************************************************************************************
# main functions
# *********************************************************************************************************************
# main play music
def play_music(ctx):
    # remove "song.mp3" file if song.mp3 exists -> song.mp3 not exist
    if os.path.isfile(current_song_mp3_path):
        os.remove(current_song_mp3_path)
    # rename "next_song.mp3" to "song.mp3" if next_song.mp3 existed -> song.mp3 exist
    if os.path.isfile(next_song_mp3_path):
        os.rename(next_song_mp3_path, current_song_mp3_path)
    # download songs
    songs_list = get_songs_list()
    if len(songs_list) > 0:
        # check if next_song.mp3 existed - play song.mp3
        if len(songs_list) > 1:
            if os.path.isfile(current_song_mp3_path):
                play_song(ctx, current_song_mp3_path)
                download_song(get_next_song(), next_song_mp3_path)
            else:
                download_song(get_current_song(), current_song_mp3_path)
                play_song(ctx, current_song_mp3_path)
                download_song(get_next_song(), next_song_mp3_path)
        if len(songs_list) == 1:
            download_song(get_current_song(), current_song_mp3_path)
            play_song(ctx, current_song_mp3_path)
    else:
        print("~~~~~~~~~ No more audio in queue ~~~~~~~~~")
        voice = ctx.voice_client
        reset_songs_list()


# play next song
def play_next(ctx):
    print("~~~~~~~~~ Inside play_next ~~~~~~~~~")
    delete_first_song()
    play_music(ctx)
