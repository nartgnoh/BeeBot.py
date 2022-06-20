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


def event_exists(events_data, event):
    if event not in events_data:
        events_data[event] = {}
    return events_data


def events_key_exists(events_data, event, key):
    if key not in events_data[event]:
        events_data[event][key] = {}
    return events_data


def check_event(events_data, event):
    if event in events_data:
        return True
    else:
        return False
