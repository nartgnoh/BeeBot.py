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


def event_exists(event, events):
    if event not in events:
        events[event] = {}


def events_key_exists(key, event, events):
    if key not in events[event]:
        events[event][key] = {}
