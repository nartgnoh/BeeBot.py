# *********************************************************************************************************************
# emojis.py
# import cogs.helper.helper_functions.emojis as emojis
# *********************************************************************************************************************

import os
import json

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
emojis_json = "/".join(list(current_directory.split('/')
                            [0:-3])) + '/resource_files/json_files/emojis.json'


def get_full_emojis_list():
    with open(emojis_json, "r") as f:
        emojis_list = json.load(f)
    return emojis_list


def check_emoji(emoji):
    emojis_list = get_full_emojis_list()
    if any(d['emoji'] == emoji for d in emojis_list):
        return True
    else:
        return False
