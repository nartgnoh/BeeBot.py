# *********************************************************************************************************************
# beebot_profiles.py
# import cogs.helper.helper_functions.beebot_profiles as beebot_profiles
# *********************************************************************************************************************

import os
import json

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))


def check_profile_exists(discord_username):
    # read beebot_profiles.json file
    beebot_profiles_json = "/".join(list(current_directory.split('/')
                                         [0:-3])) + '/resource_files/json_files/beebot_profiles.json'
    with open(beebot_profiles_json, "r") as f:
        beebot_profiles = json.load(f)
    if discord_username in beebot_profiles:
        return True
    else:
        return False
