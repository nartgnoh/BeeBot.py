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

song_mp3_path = "/".join(list(current_directory.split('/')
                              [0:-3])) + '/resource_files/music_files/song.mp3'


# get songs_list_json entire list
def get_songs_list():
    with open(songs_list_json) as f:
        return json.load(f)


# get songs_list_json first element
def get_current_song():
    return get_songs_list()[0]


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


# # get youtube_dl info
# def get_yt_dl_info():
#     current_song = get_current_song()
#     youtube_url = "https://www.youtube.com/" + current_song["url_suffix"]
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }]
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(youtube_url, download=False)['formats'][0]['url']
#         return info

# # go next
# def go_next():
#     delete_first_song()
#     return get_yt_dl_info()

# play songs
def play_songs(ctx):
    check = True
    # create song file
    song_there = os.path.isfile(song_mp3_path)
    try:
        # remove "song.mp3" file
        if song_there:
            os.remove(song_mp3_path)
    except PermissionError:
        print('~~~~~~~~~ Error in play_songs() around "song_there" ~~~~~~~~~ ')
    try:
        current_song = get_current_song()
    except:
        check = False
        print("~~~~~~~~~ No more audio in queue ~~~~~~~~~")
    if check:
        youtube_url = "https://www.youtube.com/" + current_song["url_suffix"]
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
                os.rename(file, song_mp3_path)
        voice = ctx.voice_client

        # voice.play(discord.FFmpegPCMAudio(song_mp3_path),
        #             after=lambda e: play_next(ctx))
        # voice.is_playing()


def play_next(ctx):
    print("~~~~~~~~~ Inside play_next ~~~~~~~~~")
    try:
        delete_first_song()
    except:
        print("~~~~~~~~~ Nothing left in songs_list.json ~~~~~~~~~")
    play_songs(ctx)

# # # play songs
# async def play_songs(ctx, bot):
#     current_song = get_current_song()
#     youtube_url = "https://www.youtube.com/" + current_song["url_suffix"]
#     ydl_opts = {'format': 'bestaudio/best',
#                 'postprocessors': [{
#                     'key': 'FFmpegExtractAudio',
#                     'preferredcodec': 'mp3',
#                     'preferredquality': '192',
#                 }]
#                 }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(youtube_url, download=False)[
#             'formats'][0]['url']
#         voice = ctx.voice_client
#         FFMPEG_OPTIONS = {
#             'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#         voice.is_playing()
#         voice.play(await discord.FFmpegOpusAudio.from_probe(info, **FFMPEG_OPTIONS))

    # await discord.FFmpegOpusAudio.from_probe(song, **FFMPEG_OPTIONS)
    # # calling this "download_song" function again to play next song
    # voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    # song = info['formats'][0]['url']
    # FFMPEG_OPTIONS = {
    #     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    # voice.play(await discord.FFmpegOpusAudio.from_probe(song, **FFMPEG_OPTIONS),
    #            after=lambda e: download_song(ctx, bot))
    # voice.is_playing()


# # check if songs_list_json is empty without the first element (current)
# def check_rest_songs_list():
#     with open(songs_list_json) as f:
#         if json.load(f)[1:]:
#             return True
#         else:
#             return False


# # check duration of song is under 15mins
# def check_duration(yt_json):
#     duration = datetime.strptime(yt_json['duration'], '%M:%S')
#     # if yt_json[]
