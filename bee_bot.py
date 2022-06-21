# *********************************************************************************************************************
# bee_bot.py
# *********************************************************************************************************************

import os
import discord
import sys
import traceback

from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp

# get all cog extensions
all_extensions = ['cogs.admin.admin_beebot_reset_module',
                  'cogs.beebot_profile.beebotprofilemodule',
                  'cogs.beebot_profile.lolbeebotprofilemodule',
                  # 'cogs.events.eventsmodule',
                  'cogs.games.league_of_legends.lolinfomodule',
                  'cogs.games.league_of_legends.lolprofilemodule',
                  'cogs.games.league_of_legends.lolskinsmodule',
                  'cogs.games.league_of_legends.lolclashmodule',
                  'cogs.games.league_of_legends.lolteamsmodule',
                  'cogs.games.gamesmodule',
                  # 'cogs.games.teamfight_tactics',
                  'cogs.helper.listeners.reactions_listener',
                  # 'cogs.music.playmusicmodule',
                  # 'cogs.music.viewmusicmodule',
                  'cogs.responses.emotionsmodule',
                  'cogs.responses.giveawaymodule',
                  'cogs.responses.pollsmodule',
                  'cogs.responses.responsesmodule'
                  ]


def get_prefix(bot, message):
    prefixes = ['BB ', 'bb ', 'Bb ', 'bB ']  # BeeBot exclusive
    # prefixes = ['B ', 'b ']  # BeeBot-Testing exclusive
    return commands.when_mentioned_or(*prefixes)(bot, message)


# get from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# connecting with discord with "discord intents"
intents = discord.Intents.default()
intents.members = True

# bot setup
bot = commands.Bot(command_prefix=get_prefix, description='🐝 Hello! I am BeeBot! 🐝',
                   case_insensitive=True, intents=intents, help_command=PrettyHelp())

# load extensions(cogs) listed above in [all_extensions].
if __name__ == '__main__':
    for extension in all_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print('----------------------------------------------\n'
          f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n\n')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="with BEES NUTS (type \"BB help\")"))
    print(f'BeeBot successfully logged in and booted! :D'
          '\n----------------------------------------------')


bot.run(DISCORD_TOKEN, bot=True, reconnect=True)
