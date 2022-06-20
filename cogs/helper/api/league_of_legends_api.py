# *********************************************************************************************************************
# league_of_legends_api.py
# import cogs.helper.api.league_of_legends_api as lol_api
# *********************************************************************************************************************

import os

from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError

# get riot_lol_key from .env file
load_dotenv()
LOL_KEY = os.getenv('RIOT_LOL_KEY')
lol_watcher = LolWatcher(LOL_KEY)
default_region = 'na1'


def get_version(region=default_region):
    return lol_watcher.data_dragon.versions_for_region(region)


def get_champion_list(champions_version=get_version(default_region)):
    return lol_watcher.data_dragon.champions(champions_version)


def champion_string_formatting(champion):
    return champion.replace("'", '').lower().title().replace(' ', '').strip('"')


def champion_url_by_name(champ_name):
    formatting = champ_name.replace("'", '-').replace(" ", '-').lower()
    return f"https://www.leagueoflegends.com/en-us/champions/{formatting}/"
