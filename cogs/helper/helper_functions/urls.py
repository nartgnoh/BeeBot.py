# *********************************************************************************************************************
# urls.py
# import cogs.helper.helper_functions.urls as urls
# *********************************************************************************************************************

import os
import json

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
urls_json = "/".join(list(current_directory.split('/')
                          [0:-3])) + '/resource_files/json_files/urls.json'


def get_urls_json():
    with open(urls_json, "r") as f:
        urls = json.load(f)
    return urls


def set_urls_json(data):
    with open(urls_json, 'w') as outfile:
        json.dump(data, outfile)


def new_url(url_name, data):
    urls_data = get_urls_json()
    urls_data[url_name] = data
    set_urls_json(urls_data)


def check_url(urls, url):
    if url in urls:
        return True
    else:
        return False
