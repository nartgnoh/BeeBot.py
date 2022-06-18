# bee_bot.py
import os
import discord
import sys, traceback

from discord.ext import commands
from dotenv import load_dotenv

# get all cog extensions
all_extensions = [
                # 'cogs.events.events',
                'cogs.games.league_of_legends.lolinfo',
                'cogs.games.league_of_legends.lolprofile',
                'cogs.games.league_of_legends.lolskins',
                # 'cogs.games.league_of_legends.lolclash',
                'cogs.games.league_of_legends.lolteamcomp',
                'cogs.games.games',
                # 'cogs.games.teamfight_tactics',
                'cogs.music.basic',
                # 'cogs.music.play',
                # 'cogs.music.view',
                'cogs.responses.emotions',
                'cogs.responses.poll',
                'cogs.responses.responses',
                ]
                

# get from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# connecting with discord with "discord intents"
intents = discord.Intents.default()
intents.members = True

def get_prefix(bot, message):
    prefixes = ['BB ', 'bb ', 'Bb ', 'bB '] # BeeBot exclusive
    # prefixes = ['BT ', 'bt ', 'B ', 'b '] # BeeBot-Testing exclusive

    return commands.when_mentioned_or(*prefixes)(bot, message)

# setup bot
bot = commands.Bot(command_prefix=get_prefix, description='🐝 Hello! I am BeeBot! 🐝', case_insensitive=True, intents=intents)

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