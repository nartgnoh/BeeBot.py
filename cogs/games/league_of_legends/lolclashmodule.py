# *********************************************************************************************************************
# lolclashmodule.py
# - clashadd command
# - clashremove command
# - clashview command
# - clashset command
# *********************************************************************************************************************

import os
import discord
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
owner_specific_command_name = 'Bot Admin'

# lolclashmodule class


class lolclashmodule(commands.Cog, name="LoLClashModule", description="clashadd, clashremove, clashview"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to add author from availability list
    # *********************************************************************************************************************
    @commands.command(name='clashadd', aliases=['addclash', 'aclash', 'clasha', 'clashavailable'],
                      help='➕ Add your clash availability! [Pick between: \'Sat\', \'Sun\', or \'Both\']')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def clash_add(self, ctx, availability: Optional[str]):
        # read events.json file
        event_json = "/".join(list(current_directory.split('/')
                              [0:-3])) + '/resource_files/json_files/events.json'
        with open(event_json) as f:
            data = json.load(f)
        if 'clash' not in data:
            await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        else:
            clash_event = data['clash']
            clash_date = datetime.fromtimestamp(
                clash_event['schedule'][0]['startTime'] / 1e3)
            if clash_date < datetime.now():
                await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
            else:
                if availability == None:
                    await ctx.send('Please specify either \'Sat\', \'Sun\' or \'Both\' after command! :slight_smile:')
                else:
                    availability = availability.lower().title()
                    if not availability == 'Sat' and not availability == 'Sun' and not availability == 'Both':
                        await ctx.send('Invalid input! :flushed: Please specify either \'Sat\', \'Sun\' or \'Both\' '
                                       'after command! :smile:')
                    else:
                        # check if member already registered
                        available_member = str(ctx.message.author)
                        participants = clash_event['participants']
                        if availability == 'Both':
                            avail_dict = {'Sat': 1, 'Sun': 1}
                        else:
                            avail_dict = {availability: 1}
                        if available_member in participants:
                            member = participants[available_member]
                            if member['Sat'] == 1 and member['Sun'] == 1:
                                await ctx.send('Your name was already added to the list for both days! :open_mouth:')
                            elif (member['Sat'] == 1 and availability == 'Sat') or (member['Sun'] == 1 and availability == 'Sun'):
                                await ctx.send('Your name was already added to the list for this day! :open_mouth:')
                            else:
                                participants[available_member].update(
                                    avail_dict)
                                await ctx.send("Your availability has been added to the list! :white_check_mark:")
                        else:
                            participants[available_member] = {
                                'Sat': 0, 'Sun': 0}
                            participants[available_member].update(avail_dict)
                            await ctx.send("Your availability has been added to the list! :white_check_mark:")
                        # write to events.json file
                        with open(event_json, 'w') as outfile:
                            json.dump(data, outfile)

    # *********************************************************************************************************************
    # bot command to remove author from availability list
    # *********************************************************************************************************************
    @commands.command(name='clashremove', aliases=['removeclash', 'rclash', 'clashr'],
                      help='➖ Remove your clash availability!')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def clash_remove(self, ctx, availability: Optional[str]):
        # read events.json file
        event_json = "/".join(list(current_directory.split('/')
                              [0:-3])) + '/resource_files/json_files/events.json'
        with open(event_json) as f:
            data = json.load(f)
        if 'clash' not in data:
            await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        else:
            clash_event = data['clash']
            clash_date = datetime.fromtimestamp(
                clash_event['schedule'][0]['startTime'] / 1e3)
            if clash_date < datetime.now():
                await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
            else:
                if availability == None:
                    await ctx.send('Please specify either \'Sat\', \'Sun\' or \'Both\' after command! :slight_smile:')
                else:
                    availability = availability.lower().title()
                    if not availability == 'Sat' and not availability == 'Sun' and not availability == 'Both':
                        await ctx.send('Invalid input! :flushed: Please specify either \'Sat\', \'Sun\' or \'Both\' '
                                       'after command! :smile:')
                    else:
                        # check if member already registered
                        available_member = str(ctx.message.author)
                        participants = clash_event['participants']
                        if availability == 'Both':
                            avail_dict = {'Sat': 0, 'Sun': 0}
                        else:
                            avail_dict = {availability: 0}
                        if available_member not in participants:
                            await ctx.send('Your name wasn\'t on the list. :thinking: Add it with the "addclash" command! :smile:')
                        else:
                            member = participants[available_member]
                            if (member['Sat'] == 0 and availability == 'Sat') or (member['Sun'] == 0 and availability == 'Sun'):
                                await ctx.send('You\'re already not signed up for this day! :open_mouth:')
                            else:
                                participants[available_member].update(
                                    avail_dict)
                                if participants[available_member] == {'Sat': 0, 'Sun': 0}:
                                    participants.pop(available_member)
                                # write to events.json file
                                with open(event_json, 'w') as outfile:
                                    json.dump(data, outfile)
                                await ctx.send('Your name was removed from the availability list. :slight_smile:')

    # *********************************************************************************************************************
    # bot command to view clash availability list
    # *********************************************************************************************************************

    @commands.command(name='clashview', aliases=['viewclash', 'clashv', 'vclash'],
                      help='📜 View list of people available for clash.')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def clash_view(self, ctx):
        # read events.json file
        event_json = "/".join(list(current_directory.split('/')
                              [0:-3])) + '/resource_files/json_files/events.json'
        with open(event_json) as f:
            data = json.load(f)
        clash = data['clash']
        date = datetime.fromtimestamp(clash['schedule'][0]['startTime'] / 1e3)
        if not clash['participants']:
            await ctx.send('No one has added their availability yet! :cry: Add yours with the \"addclash\" command! :smile:')
        elif date < datetime.now():
            await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        else:
            available_days = {'Saturday': [], 'Sunday': []}
            for member in clash['participants']:
                # format string
                member_name = '#'.join(member.split("#")[:-1])
                if clash['participants'][member]['Sat'] == 1:
                    available_days['Saturday'].append(member_name)
                if clash['participants'][member]['Sun'] == 1:
                    available_days['Sunday'].append(member_name)
            # *********
            # | embed |
            # *********
            embed = Embed(title="Clash List!",
                          description="Here are the people that signed up for Clash weekend! :D",
                          colour=ctx.author.colour)
            # embed thumbnail
            file = discord.File(
                f"resource_files/image_files/thumbnails/lolclash_thumb.png", filename="image.png")
            embed.set_thumbnail(url='attachment://image.png')
            # embed fields
            for day in available_days:
                if available_days[day]:
                    embed.add_field(name=f"{day}:", value=', '.join(
                        available_days[day]), inline=False)
            await ctx.send(file=file, embed=embed)

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
        clash_sorted = dict(
            sorted(clash_dict.items(), key=lambda item: item[1]))
        deadline_current_clash = list(clash_sorted.items())[1]
        # get all clash data using the 'id' for the upcoming tournament
        current_clash = {}
        for clash in clash_data:
            if clash['id'] == deadline_current_clash[0]:
                current_clash = clash
                break
        # add 'participants' field
        current_clash['participants'] = {'Sat': [], 'Sun': []}
        # read events.json file
        event_json = "/".join(list(current_directory.split('/')
                              [0:-3])) + '/resource_files/json_files/events.json'
        with open(event_json) as f:
            data = json.load(f)
        # check if 'clash' key exists
        if 'clash' in data.keys():
            # update current clash with the next clash
            date = datetime.fromtimestamp(
                data['clash']['schedule'][0]['startTime'] / 1e3)
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
    bot.add_cog(lolclashmodule(bot))
