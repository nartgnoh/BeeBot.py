# *********************************************************************************************************************
# lolclashmodule.py
# - clashadd command
# - clashremove command
# - clashview command
# - clashset command
# *********************************************************************************************************************

import os
import discord
import cogs.helper.constants.lol_constants as lol_constants
import cogs.helper.helper_functions.timezones as timezones
import cogs.helper.helper_functions.events as events
import cogs.helper.helper_functions.beebot_profiles as beebot_profiles

from discord.ext import commands
from discord import Embed
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError

# get riot_lol_key from .env file
load_dotenv()
LOL_KEY = os.getenv('RIOT_LOL_KEY')
lol_watcher = LolWatcher(LOL_KEY)
default_region = 'na1'

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# lolclashmodule class


class lolclashmodule(commands.Cog, name="LoLClashModule", description="clashadd, clashremove, clashview"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to add author from availability list
    # *********************************************************************************************************************
    @commands.command(name='clashadd', aliases=['addclash', 'aclash', 'clasha', 'clashavailable', 'clash+', '+clash', '➕'],
                      help=f"➕ Add your Clash availability! [Pick between: \'Sat\', \'Sun\', or \'Both\']\n\n"
                      f"[Valid Roles: {', '.join(lol_constants.lol_roles())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def clash_add(self, ctx, availability: Optional[str], *roles):
        events_data = events.get_events_json()
        if not events.check_event(events_data, 'clash'):
            return await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        clash_event = events_data['clash']
        clash_date = datetime.fromtimestamp(
            clash_event['schedule'][0]['startTime'] / 1e3)
        if clash_date < datetime.now():
            return await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        if availability == None:
            return await ctx.send('Please specify either \'Sat\', \'Sun\' or \'Both\' after command! :slight_smile:')
        availability = availability.lower().title()
        if not availability == 'Sat' and not availability == 'Sun' and not availability == 'Both' and availability not in lol_constants.lol_roles():
            return await ctx.send('Invalid input! :flushed: Please specify either \'Sat\', \'Sun\', \'Both\', or role(s) '
                                  'after command! :smile:')
        available_member = str(ctx.message.author)
        participants = clash_event['participants']
        roles = list(roles)
        avail_dict = {}
        if availability in lol_constants.lol_roles():
            roles = [availability.lower()] + roles
        elif availability == 'Both':
            avail_dict = {'Sat': 1, 'Sun': 1}
        else:
            avail_dict = {availability: 1}
        # add roles
        roles_list = []
        if roles:
            for role in roles:
                if role.title() in lol_constants.lol_roles():
                    roles_list.append(role.lower())
            roles_list = list(dict.fromkeys(roles_list))
        role_msg = ''
        if roles_list:
            role_msg = 'and preferred role(s) '
            beebot_profiles_data = beebot_profiles.get_beebot_profiles_json()
            # add member's roles
            beebot_profiles_data = beebot_profiles.beebot_profile_exists(
                beebot_profiles_data, available_member)
            beebot_profiles_data = beebot_profiles.beebot_profile_key_exists(
                beebot_profiles_data, available_member, "league_of_legends")
            beebot_profiles_data[available_member]["league_of_legends"][
                'preferred_role(s)'] = roles_list
            beebot_profiles_data = beebot_profiles.set_beebot_profiles_json(
                beebot_profiles_data)
        # check if member already registered
        if available_member in participants and (availability == 'Sat' or availability == 'Sun' or availability == 'Both'):
            member = participants[available_member]
            if member['Sat'] == 1 and member['Sun'] == 1 and not roles_list:
                await ctx.send('Your name was already added to the list for both days! :open_mouth:')
            elif (member['Sat'] == 1 and availability == 'Sat') or (member['Sun'] == 1 and availability == 'Sun') and not roles_list:
                await ctx.send('Your name was already added to the list for this day! :open_mouth:')
            else:
                participants[available_member].update(
                    avail_dict)
                await ctx.send(f"Your availability {role_msg}has been updated! :white_check_mark:")
        elif availability in lol_constants.lol_roles() and roles_list:
            await ctx.send(f"Your preferred role(s) has been updated! :white_check_mark:")
        else:
            participants[available_member] = {
                'Sat': 0, 'Sun': 0}
            participants[available_member].update(avail_dict)
            await ctx.send(f"Your availability {role_msg}has been updated! :white_check_mark:")
        events.set_events_json(events_data)

    # *********************************************************************************************************************
    # bot command to remove author from availability list
    # *********************************************************************************************************************
    @commands.command(name='clashremove', aliases=['removeclash', 'rclash', 'clashr', 'clash-', '-clash', '➖'],
                      help='➖ Remove your Clash availability! [Pick between: \'Sat\', \'Sun\', or \'Both\']')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def clash_remove(self, ctx, availability: Optional[str]):
        events_data = events.get_events_json()
        if not events.check_event(events_data, 'clash'):
            return await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        clash_event = events_data['clash']
        clash_date = datetime.fromtimestamp(
            clash_event['schedule'][0]['startTime'] / 1e3)
        if clash_date < datetime.now():
            return await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        if availability == None:
            return await ctx.send('Please specify either \'Sat\', \'Sun\' or \'Both\' after command! :slight_smile:')
        availability = availability.lower().title()
        if not availability == 'Sat' and not availability == 'Sun' and not availability == 'Both':
            return await ctx.send('Invalid input! :flushed: Please specify either \'Sat\', \'Sun\' or \'Both\' '
                                  'after command! :smile:')
        # check if member already registered
        available_member = str(ctx.message.author)
        participants = clash_event['participants']
        if availability == 'Both':
            avail_dict = {'Sat': 0, 'Sun': 0}
        else:
            avail_dict = {availability: 0}
        if available_member not in participants:
            return await ctx.send('Your name wasn\'t on the list. :thinking: Add it with the "addclash" command! :smile:')
        member = participants[available_member]
        if (member['Sat'] == 0 and availability == 'Sat') or (member['Sun'] == 0 and availability == 'Sun'):
            await ctx.send('You\'re already not signed up for this day! :open_mouth:')
        else:
            participants[available_member].update(
                avail_dict)
            if participants[available_member] == {'Sat': 0, 'Sun': 0}:
                participants.pop(available_member)
            events.set_events_json(events_data)
            await ctx.send('Your name was removed from the availability list for this day(s). :slight_smile:')

    # *********************************************************************************************************************
    # bot command to view clash availability list
    # *********************************************************************************************************************
    @commands.command(name='clashview', aliases=['viewclash', 'clashv', 'vclash', 'clashavailability', '📜'],
                      help='📜 View list of people available for Clash.')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def clash_view(self, ctx):
        events_data = events.get_events_json()
        clash = events_data['clash']
        date = datetime.fromtimestamp(clash['schedule'][0]['startTime'] / 1e3)
        if not clash['participants']:
            return await ctx.send('No one has added their availability yet! :cry: Add yours with the \"addclash\" command! :smile:')
        elif date < datetime.now():
            return await ctx.send('There\'s currently no clash scheduled! :open_mouth: Try again next clash!')
        available_days = {'Saturday': [], 'Sunday': []}
        for member in clash['participants']:
            beebot_profiles_data = beebot_profiles.get_beebot_profiles_json()
            fields = []
            if beebot_profiles.check_beebot_profile(beebot_profiles_data, member):
                if beebot_profiles.check_beebot_profile(beebot_profiles_data[member], 'league_of_legends'):
                    if beebot_profiles.check_beebot_profile(beebot_profiles_data[member]['league_of_legends'], 'preferred_role(s)'):
                        if beebot_profiles_data[member]['league_of_legends']['preferred_role(s)']:
                            # add roles
                            fields.append(
                                f"preferred role(s): *{', '.join(beebot_profiles_data[member]['league_of_legends']['preferred_role(s)'])}*")
            # set fields
            if not fields:
                fields = ''
            else:
                fields = f"[{' | '.join(fields)}]"
            # format string
            member_name = '#'.join(member.split("#")[:-1])
            if clash['participants'][member]['Sat'] == 1:
                available_days['Saturday'].append(
                    f"- ***{member_name}*** {fields}")
            if clash['participants'][member]['Sun'] == 1:
                available_days['Sunday'].append(
                    f"- ***{member_name}*** {fields}")
        # *********
        # | embed |
        # *********
        embed = Embed(title="Clash List",
                      description=f"Here are the signups for the next Clash weekend!\n"
                      f"Last day to signup is;\n"
                      f"*{date.astimezone(timezones.get_pacific_timezone()).strftime('%A, %B %-d, %Y @ %-I:%M%p (%Z)')}*\n"
                      f"*{date.astimezone(timezones.get_eastern_timezone()).strftime('%A, %B %-d, %Y @ %-I:%M%p (%Z)')}*",
                      colour=ctx.author.colour)
        # embed thumbnail
        file = discord.File(
            f"resource_files/image_files/thumbnails/lolclash_thumb.png", filename="image.png")
        embed.set_thumbnail(url='attachment://image.png')
        # embed fields
        for day in available_days:
            if available_days[day]:
                if day == 'Saturday':
                    clash_date = date - timedelta(days=1)
                else:
                    clash_date = date
                embed.add_field(name=clash_date.astimezone(timezones.get_pacific_timezone()).strftime(
                    '%A, %B %-d, %Y:'), value='\n'.join(available_days[day]), inline=False)
        await ctx.send(file=file, embed=embed)

    # *********************************************************************************************************************
    # bot command to set clash date
    # *********************************************************************************************************************
    @commands.command(name='clashset', aliases=['setclash', 'sclash', 'clashs'],
                      help='🛡️ Setup next Clash. [Admin Specific]')
    # only VERY specific roles can use this command
    @commands.has_role(admin_specific_command_name)
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
        current_clash['participants'] = {}
        events_data = events.get_events_json()
        # check if 'clash' key exists
        if events.check_event(events_data, 'clash'):
            # update current clash with the next clash
            date = datetime.fromtimestamp(
                events_data['clash']['schedule'][0]['startTime'] / 1e3)
            if date < datetime.now():
                events_data['clash'] = current_clash
                events.set_events_json(events_data)
                await ctx.send("Updated clash!")
            else:
                await ctx.send("Hold your horses.. The upcoming clash hasn't even happened yet!")
        # add 'clash' key if it doesn't exist
        else:
            events_data['clash'] = current_clash
            events.set_events_json(events_data)
            await ctx.send("New clash key!")


def setup(bot):
    bot.add_cog(lolclashmodule(bot))
