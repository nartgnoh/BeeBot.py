# *********************************************************************************************************************
# basic.py
# - wip
# *********************************************************************************************************************

import os
import discord
import random

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

# basic class
class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # *********************************************************************************************************************
    # bot command to join voice channel
    # *********************************************************************************************************************
    @commands.command(name='join', aliases=['joincall', '🔊'], help='🔊 Beebot joins your voice channel!')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def command_name(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
    
    # *********************************************************************************************************************
    # bot command to leave voice channel and deletes queue
    # *********************************************************************************************************************
    @commands.command(name='leave', aliases=['stopaudio', 'leavecall', 'deletequeue', 'disconnect', '🔈'],
                help='🔈 Beebot leaves voice channel and deletes current queue. [Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

        # voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        # if voice.is_connected():
        #     new_yt_links_file = open("resource_files/music_bot_files/yt_links.txt", "w")
        #     yt_current_file = open("resource_files/music_bot_files/yt_current.txt", "w")
        #     await ctx.send("Ok I'll leave. :cry:")
        #     voice.stop()
        #     server = ctx.message.guild.voice_client
        #     await server.disconnect()
        # else:
        #     await ctx.send("BeeBot is not connected to a voice channel. :thinking:")

def setup(bot):
    bot.add_cog(basic(bot))