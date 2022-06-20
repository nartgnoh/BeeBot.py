# *********************************************************************************************************************
# emojis.py
# import cogs.helper.helper_functions.emojis as emojis
# *********************************************************************************************************************

import os
import cogs.helper.constants.emoji_constants as emoji_constants

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))


def check_emoji_exists(emoji):
    emojis_list = emoji_constants.emojis_list()
    if any(d['emoji'] == emoji for d in emojis_list):
        return True
    else:
        return False
