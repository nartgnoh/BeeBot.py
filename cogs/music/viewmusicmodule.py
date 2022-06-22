# *********************************************************************************************************************
# viewmusicmodule.py
# - viewcurrent command
# - viewnext command
# - viewqueue command
# *********************************************************************************************************************

import os
import discord
import cogs.helper.helper_functions.music as music_helper

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# viewmusicmodule class


class viewmusicmodule(commands.Cog, name="ViewMusicModule", description=""):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to view current audio
    # *********************************************************************************************************************
    @commands.command(name='viewcurrent', aliases=['currentview', 'currentaudio', 'vcurrent', 'cview', 'current', '🎵'],
                      help='🎵 View the current audio!')
    async def view_current(self, ctx):
        if not music_helper.get_songs_list():
            await ctx.send("There's no current audio! :open_mouth: Add a song with the \"play\" command! :smile:")
        else:
            current_song = music_helper.get_current_song()
            # *********
            # | embed |
            # *********
            embed = Embed(title=f"🎵 Current song 🎵\n{current_song['title']}",
                          description=f"By: {current_song['channel']}\nDuration: {current_song['duration']}",
                          colour=ctx.author.colour)
            # embed thumbnail
            thumb_url = current_song['thumbnails'][0]
            embed.set_thumbnail(url=thumb_url)
            await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to view next audio
    # *********************************************************************************************************************
    @commands.command(name='viewnext', aliases=['nextview', 'nextaudio', 'vnext', 'nview', '🎼'],
                      help='🎼 View the next audio!')
    async def view_next(self, ctx):
        if not music_helper.get_songs_list()[1:]:
            await ctx.send("There's no next audio! :open_mouth: Add another song with the \"play\" command! :smile:")
        else:
            next_song = music_helper.get_next_song()
            # *********
            # | embed |
            # *********
            embed = Embed(title=f"🎼 Next song is 🎼\n{next_song['title']}",
                          description=f"By: {next_song['channel']}\nDuration: {next_song['duration']}",
                          colour=ctx.author.colour)
            # embed thumbnail
            thumb_url = next_song['thumbnails'][0]
            embed.set_thumbnail(url=thumb_url)
            await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to view current queue
    # *********************************************************************************************************************
    @commands.command(name='viewqueue', aliases=['queueview', 'currentqueue', 'viewq', 'qview', 'queue'],
                      help='🎶 View the current queue!')
    async def current_queue(self, ctx):
        if not music_helper.get_songs_list()[1:]:
            await ctx.send('There is not audio in the queue! :flushed: Try the "play" command to add a song! :smile:')
        else:
            songs_list = music_helper.get_songs_list()
            song_names_list = []
            count = 0
            for song in songs_list:
                count += 1
                song_names_list.append(f"{count}: {song['title']}")
            # *********
            # | embed |
            # *********
            embed = Embed(title="🎶 Current Queue 🎶",
                          description='\n'.join(song_names_list),
                          colour=ctx.author.colour)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(viewmusicmodule(bot))
