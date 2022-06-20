# *********************************************************************************************************************
# events.py
# import cogs.helper.helper_functions.events as events
# *********************************************************************************************************************

import os
import json

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
events_json = "/".join(list(current_directory.split('/')
                            [0:-3])) + '/resource_files/json_files/events.json'


def get_events_json():
    with open(events_json, "r") as f:
        events = json.load(f)
    return events


def set_events_json(data):
    with open(events_json, 'w') as outfile:
        json.dump(data, outfile)


def new_event(events, event, data):
    events[event] = data


def event_exists(events, event):
    if event not in events:
        events[event] = {}


def events_key_exists(events, event, key):
    if key not in events[event]:
        events[event][key] = {}


def check_event(events, event):
    if event in events:
        return True
    else:
        return False
