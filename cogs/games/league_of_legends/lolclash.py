# *********************************************************************************************************************
# lolclash.py
# - (wip)
# *********************************************************************************************************************

import os
import discord
import random
import json

from discord.ext import commands
from discord import Embed
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError

# get riot_lol_key from .env file
load_dotenv()
LOL_KEY = os.getenv('RIOT_LOL_KEY')
lol_watcher = LolWatcher(LOL_KEY)
default_region = 'na1'

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

# lolclash class
class lolclash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # # *********************************************************************************************************************
    # # bot command to add author from availability list
    # # *********************************************************************************************************************
    # @commands.command(name='clashadd', aliases=['addclash', 'aclash', 'clasha', 'clashavailable'],
    #             help='Add your clash availability! [Pick between: \'Sat\', \'Sun\', or \'Both\']')
    # # only specific roles can use this command
    # @commands.has_role(role_specific_command_name)
    # async def clash_add(ctx, *, date: Optional[str]):
    #     try:
    #         # available member for clash
    #         available_member = ctx.message.author
    #         if date == None:
    #             await ctx.send('Please specify either \'Sat\', \'Sun\' or \'Both\' after command! :smile:')
    #         else:
    #             # help case sensitivity
    #             date = date.lower()
    #             # if not sun or sat (the usual clash days)
    #             if not date == 'sat' and not date == 'sun' and not date == 'both':
    #                 await ctx.send('Invalid input! :flushed: Please specify either \'Sat\', \'Sun\' or \'Both\' '
    #                             'after command! :smile:')
    #             else:
    #                 json_functions.read_json_file()
    #                 # with open('resource_files/clash_files/clash_available.txt') as f:
    #                 #     data = f.read()
    #                 # avail_dict = ast.literal_eval(data)

    #                 # # read the "clash_dates.txt" file and check if the given date >= present
    #                 # clash_dates_file = open("resource_files/clash_files/clash_dates.txt")
    #                 # clash_dates_file.flush()
    #                 # new_clash_date = clash_dates_file.readline()
    #                 # clash_date_convert = datetime.strptime(new_clash_date, '%d-%m-%Y %H:%M')
    #                 # if clash_date_convert >= present:
    #                 #     if not date == 'both':
    #                 #         # check if member is already in the "clash_available.txt" file
    #                 #         check = False
    #                 #         # capitalize "Sun" or "Sat"
    #                 #         date = date.capitalize()
    #                 #         text_input = str(available_member.id) + date + ' : ' + str(available_member.display_name) + '\n'
    #                 #         check_input = str(available_member.id) + date
    #                 #         clash_available_file = open("resource_files/clash_files/clash_available.txt")
    #                 #         check_txt = clash_available_file.readlines()
    #                 #         # check if member is already in the "clash_available.txt" file
    #                 #         for lines in check_txt:
    #                 #             # look at only the id and date from "lines"
    #                 #             only_id = re.sub("\D", "", lines)
    #                 #             after_id = lines[len(only_id):]
    #                 #             only_date = after_id[:3]
    #                 #             # new line
    #                 #             new_line = only_id + only_date
    #                 #             if check_input == new_line:
    #                 #                 check = True
    #                 #         # if member is already in the "clash_available.txt" file
    #                 #         if check is True:
    #                 #             await ctx.send('Your name was already added to the list for this day! :open_mouth:')
    #                 #         # if member is NOT in the document, add them to the "clash_available.txt" file
    #                 #         else:
    #                 #             clash_available_file_a = open("resource_files/clash_files/clash_available.txt", "a")
    #                 #             clash_available_file_a.write(text_input)
    #                 #             clash_available_file_a.close()
    #                 #             await ctx.send('Your availability has been added to the list! :white_check_mark:')
    #                 #     else:
    #                 #         date = 'Sat'
    #                 #         # check specific days
    #                 #         check_sat = False
    #                 #         check_sun = False
    #                 #         text_sat = str(available_member.id) + 'Sat' + ' : ' + str(available_member.display_name) + '\n'
    #                 #         text_sun = str(available_member.id) + 'Sun' + ' : ' + str(available_member.display_name) + '\n'
    #                 #         # check if sat and/or sun already exist
    #                 #         for x in range(0, 2):
    #                 #             check_input = str(available_member.id) + date
    #                 #             clash_available_file = open("resource_files/clash_files/clash_available.txt")
    #                 #             check_txt = clash_available_file.readlines()
    #                 #             # check if member is already in the "clash_available.txt" file
    #                 #             for lines in check_txt:
    #                 #                 # look at only the id and date from "lines"
    #                 #                 only_id = re.sub("\D", "", lines)
    #                 #                 after_id = lines[len(only_id):]
    #                 #                 only_date = after_id[:3]
    #                 #                 # new line
    #                 #                 new_line = only_id + only_date
    #                 #                 if check_input == new_line and date == 'Sat':
    #                 #                     check_sat = True
    #                 #                 if check_input == new_line and date == 'Sun':
    #                 #                     check_sun = True
    #                 #             date = 'Sun'
    #                 #         # if member is already in the "clash_available.txt" file
    #                 #         if check_sat is True and check_sun is True:
    #                 #             await ctx.send('Your name was already added to the list for these days! :open_mouth:')
    #                 #         # if member is NOT in the document for SUN, add them to the "clash_available.txt" file
    #                 #         elif check_sat is True and check_sun is False:
    #                 #             clash_available_file_a = open("resource_files/clash_files/clash_available.txt", "a")
    #                 #             clash_available_file_a.write(text_sun)
    #                 #             clash_available_file_a.close()
    #                 #             await ctx.send('Your availability has been added to the list! :white_check_mark:')
    #                 #         # if member is NOT in the document for SAT, add them to the "clash_available.txt" file
    #                 #         elif check_sat is False and check_sun is True:
    #                 #             clash_available_file_a = open("resource_files/clash_files/clash_available.txt", "a")
    #                 #             clash_available_file_a.write(text_sat)
    #                 #             clash_available_file_a.close()
    #                 #             await ctx.send('Your availability has been added to the list! :white_check_mark:')
    #                 #         # if member is NOT in the document for BOTH, add them to the "clash_available.txt" file
    #                 #         else:
    #                 #             clash_available_file_a = open("resource_files/clash_files/clash_available.txt", "a")
    #                 #             clash_available_file_a.write(text_sat)
    #                 #             clash_available_file_a.write(text_sun)
    #                 #             clash_available_file_a.close()
    #                             await ctx.send('Your availability has been added to the list! :white_check_mark:')
    #     except:
    #         await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')


    # # bot command to remove author from availability list
    # @bot.command(name='clashremove', aliases=['removeclash', 'rclash', 'clashr'],
    #              help='Remove your clash availability!')
    # # only specific roles can use this command
    # @commands.has_role(role_specific_command_name)
    # async def clash_remove(ctx, *, date: Optional[str]):
    #     try:
    #         # available member for clash
    #         available_member = ctx.message.author
    #         if date == None:
    #             await ctx.send('Please specify either \'Sat\' or \'Sun\' after command! :smile:')
    #         else:
    #             # check if member is in the "clash_available.txt" file
    #             check = False
    #             # help case sensitivity
    #             date = date.lower()
    #             # if not sun or sat (the usual clash days)
    #             if not date == 'sat' and not date == 'sun':
    #                 await ctx.send('Invalid input! :flushed: Please specify either \'Sat\' or \'Sun\' '
    #                                'after command! :smile:')
    #             else:
    #                 # read the "clash_dates.txt" file and check if the given date >= present
    #                 clash_dates_file = open("resource_files/clash_files/clash_dates.txt")
    #                 clash_dates_file.flush()
    #                 new_clash_date = clash_dates_file.readline()
    #                 clash_date_convert = datetime.strptime(new_clash_date, '%d-%m-%Y %H:%M')
    #                 if clash_date_convert >= present:
    #                     # capitalize "Sun" and "Sat"
    #                     date = date.capitalize()
    #                     text_input = str(available_member.id) + date + ' : ' + str(available_member.display_name) + '\n'
    #                     check_input = str(available_member.id) + date
    #                     clash_available_file = open("resource_files/clash_files/clash_available.txt")
    #                     check_txt = clash_available_file.readlines()
    #                     # check if member is in the "clash_available.txt" file
    #                     for lines in check_txt:
    #                         # look at only the id and date from "lines"
    #                         only_id = re.sub("\D", "", lines)
    #                         after_id = lines[len(only_id):]
    #                         only_date = after_id[:3]
    #                         # new line
    #                         new_line = only_id + only_date
    #                         if check_input == new_line:
    #                             check = True
    #                     # if member is in the "clash_available.txt" file
    #                     if check == True:
    #                         # new array to store file
    #                         new_array_with_remove = []
    #                         # find the member and delete them
    #                         for lines in check_txt:
    #                             if text_input == lines:
    #                                 lines = lines.replace(lines, "")
    #                             # add the other names from the text file into "new_array_with_remove"
    #                             new_array_with_remove.append(lines)
    #                         # close file
    #                         clash_available_file.close()
    #                         # create new text file with the same name
    #                         new_clash_available_file = open('resource_files/clash_files/clash_available.txt', 'w')
    #                         # write array into new file
    #                         for lines in new_array_with_remove:
    #                             new_clash_available_file.write(lines)
    #                         new_clash_available_file.close()
    #                         await ctx.send('Your name was removed from the availability list. :slight_smile:')
    #                     else:
    #                         await ctx.send('Your name wasn\'t on the availability list. :thinking: '
    #                                        'Add it with the "addclash" command! :smile:')
    #     except:
    #         await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')

    # *********************************************************************************************************************
    # bot command to view clash availability list
    # *********************************************************************************************************************
    @commands.command(name='clashview', aliases=['viewclash', 'clashv', 'vclash'],
                 help='~ View list of people available for clash.')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def clash_view(self, ctx):
        # read events.json file
        event_json = "/".join(list(current_directory.split('/')[0:-3])) + '/resource_files/json_files/events.json'
        with open(event_json) as f:
            data = json.load(f)

        clash = data['clash']
        date = datetime.fromtimestamp(clash['schedule'][0]['startTime'] / 1e3)

        if not clash['participants']:
            await ctx.send('No one has added their availability yet! :cry: Add yours with the \"addclash\" command! :smile:')
        elif date > datetime.now():
            await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        else:

            # set initals to embed
            embed = Embed(title="The :",
                colour=ctx.author.colour)

            for party in range(len(teams_list)):
                team_number += 1
                # check if element is not empty
                if teams_list[teams]:
                    # add a new "Team" field to the embed
                    embed.add_field(name=f"Team {team_number}:", value=f"{teams_list[teams][:-2]}", inline=False)

            await ctx.send(embed=embed)


        #     # check if "clash_dates.txt" has a valid date
        #     new_clash_date = clash_dates_file.readline()
        #     clash_date_convert = datetime.strptime(new_clash_date, '%d-%m-%Y %H:%M')
        #     if clash_date_convert >= present:
        #         # check that "clash_availability.txt" file is not empty
        #         ca_check = Path(r'{}/resource_files/clash_files/clash_available.txt'.format(parent_dir))
        #         if not ca_check.stat().st_size == 0:
        #             # add lines in "clash_availability.txt" to a "clash_array"
        #             for lines in clash_available_file:
        #                 lines = lines.rstrip().lstrip('0123456789')
        #                 clash_array.append(lines)
        #             # alphabetize "clash_array"
        #             clash_array = sorted(clash_array, key=str.lower)
        #             # sort "clash_array" into "saturday" and "sunday"
        #             saturday = 'Saturday : '
        #             sunday = 'Sunday : '
        #             for key in clash_array:
        #                 if key.startswith('Sat :'):
        #                     saturday = saturday + key[6:] + ', '
        #                 elif key.startswith('Sun : '):
        #                     sunday = sunday + key[6:] + ', '
        #             # add "saturday" and "sunday" to "clash_message"
        #             clash_message = saturday[:-2] + '\n' + sunday[:-2]
        #             await ctx.send('The people available for clash are:\n{}'.format(clash_message))
        #     

    # *********************************************************************************************************************
    # bot command to set clash date
    # *********************************************************************************************************************
    @commands.command(name='clashset', aliases=['setclash', 'sclash', 'clashs'],
                 help='~ Set next clash. [Format: DD-MM-YYYY HH:MM, Role Specific]')
    # only VERY specific roles can use this command
    @commands.has_role(owner_specific_command_name)
    async def clash_set(self, ctx):
        # API call
        clash_data = lol_watcher.clash.tournaments(default_region)
        # get dictionary of upcoming clash tournaments
        clash_dict = {}
        for clash in clash_data:
            clash_dict[clash['id']] = (clash['schedule'][0]['startTime'])
        # sort dictionary and only keep the next tournament's "Sunday" dates
        clash_sorted = dict(sorted(clash_dict.items(), key=lambda item: item[1]))
        deadline_current_clash = list(clash_sorted.items())[1]
        # get all clash data using the 'id' for the upcoming tournament
        current_clash = {}
        for clash in clash_data:
            if clash['id'] == deadline_current_clash[0]:
                current_clash = clash
                break
        # add 'participants' field
        current_clash['participants'] = []

        # read events.json file
        event_json = "/".join(list(current_directory.split('/')[0:-3])) + '/resource_files/json_files/events.json'
        with open(event_json) as f:
            data = json.load(f)

        # check if 'clash' key exists
        if 'clash' in data.keys():
            # update current clash with the next clash
            date = datetime.fromtimestamp(data['clash']['schedule'][0]['startTime'] / 1e3)
            if date < datetime.now():
                data['clash'] = current_clash
                with open(event_json, 'w') as outfile:
                    json.dump(data, outfile)
                await ctx.send("Updated clash!")
            else:
                await ctx.send("Hold your horses.. The upcoming clash hasn't even happened yet!")
        # add 'clash' key if it doesn't exist
        else:
            data['clash'] = current_clash
            with open(event_json, 'w') as outfile:
                json.dump(data, outfile)
            await ctx.send("New clash key!")

def setup(bot):
    bot.add_cog(lolclash(bot))