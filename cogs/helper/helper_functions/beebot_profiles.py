# *********************************************************************************************************************
# beebot_profiles.py
# import cogs.helper.helper_functions.beebot_profiles as beebot_profiles
# *********************************************************************************************************************

import os
import json

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
beebot_profiles_json = "/".join(list(current_directory.split('/')
                                     [0:-3])) + '/resource_files/json_files/beebot_profiles.json'


def get_beebot_profiles_json():
    with open(beebot_profiles_json, "r") as f:
        beebot_profiles = json.load(f)
    return beebot_profiles


def update_beebot_profiles_json(data):
    with open(beebot_profiles_json, 'w') as outfile:
        json.dump(data, outfile)


def beebot_profile_exists(discord_username, beebot_profiles):
    if discord_username not in beebot_profiles:
        beebot_profiles[discord_username] = {}


def beebot_profile_key_exists(key, discord_username, beebot_profiles):
    if key not in beebot_profiles[discord_username]:
        beebot_profiles[discord_username][key] = {}
