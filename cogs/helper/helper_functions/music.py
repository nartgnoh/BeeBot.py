# *********************************************************************************************************************
# music.py
# import cogs.helper.helper_functions.music as music_helper
# *********************************************************************************************************************

import os
import json

from youtube_search import YoutubeSearch

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
songs_list_json = "/".join(list(current_directory.split('/')
                                [0:-3])) + '/resource_files/music_files/songs_list.json'


# *********************************************************************************************************************
# helper functions
# *********************************************************************************************************************
# get songs_list_json entire list
def get_songs_list():
    with open(songs_list_json) as f:
        return json.load(f)


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
