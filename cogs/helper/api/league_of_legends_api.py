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

# def get_summoner_match_history_20(summoner_id):

# http://ddragon.leagueoflegends.com/cdn/12.11.1/data/en_US/champion.json
def champion_string_formatting(champion):
    check = champion.replace("'", '').lower().title().replace(' ', '').strip('"')
    if check == 'Kogmaw' or check == 'Reksai':
        return champion.lower().title().replace(' ', '').replace("'", '').strip('"')
    elif check == 'Wukong': return 'MonkeyKing'
    elif check == 'JarvanIv' or check == 'J4': return 'JarvanIV'
    elif check == 'Mf': return 'MissFortune'
    elif check == 'Ez': return 'Ezreal'
    elif check == 'Heimer' or check =='Donger': return 'Herimerdinger'
    elif check == 'Cass': return 'Cassiopeia'
    elif check == 'Tk': return 'TahmKench'
    elif check == 'Tf': return 'TwistedFate'
    elif check == 'Asol': return 'AurelionSol'
    elif check == 'Cait': return 'Caitlyn'
    elif check == 'RenataGlasc': return 'Renata'
    return champion.replace('.', ' ').replace("'", '').lower().title().replace(' ', '').strip('"')


def champion_url_by_name(champ_name):
    formatting = champ_name.replace("'", '-').replace(" ", '-').replace('.', '').lower()
    return f"https://www.leagueoflegends.com/en-us/champions/{formatting}/"
