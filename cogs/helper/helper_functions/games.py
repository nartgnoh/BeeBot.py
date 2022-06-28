# *********************************************************************************************************************
# games.py
# import cogs.helper.helper_functions.games as games
# *********************************************************************************************************************

import os
import json

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
games_ideas_json = "/".join(list(current_directory.split('/')
                                 [0:-3])) + '/resource_files/json_files/game_ideas.json'
games_json = "/".join(list(current_directory.split('/')
                           [0:-3])) + '/resource_files/json_files/games.json'


def get_games_json():
    with open(games_json, "r") as f:
        games = json.load(f)
    return games


def get_game_ideas_json():
    with open(games_ideas_json, "r") as f:
        game_ideas = json.load(f)
    return game_ideas


def set_games_json(data):
    with open(games_json, 'w') as outfile:
        json.dump(data, outfile)


def check_games(games_data, games):
    if games in games_data:
        return True
    else:
        return False
