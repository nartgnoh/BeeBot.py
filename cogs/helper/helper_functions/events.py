# *********************************************************************************************************************
# events.py
# import cogs.helper.helper_functions.events as events
# *********************************************************************************************************************

import os
import json

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
