# *********************************************************************************************************************
# events.py
# *********************************************************************************************************************

import os
import json
import cogs.helper.constants.emoji_constants as emoji_constants

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))


def check_event_exists(event):
    # read events.json file
    events_json = "/".join(list(current_directory.split('/')
                                [0:-3])) + '/resource_files/json_files/events.json'
    with open(events_json, "r") as f:
        events = json.load(f)
    if event in events:
        return True
    else:
        return False
