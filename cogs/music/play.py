# *********************************************************************************************************************
# play.py
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

# play class
class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # *********************************************************************************************************************
    # bot command to play Youtube Audio
    # *********************************************************************************************************************
    @commands.command(name='play', aliases=['playaudio', 'playsong'],
             help='▶️ Plays YouTube audio! Provide YouTube search or link! [Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def play(ctx, *, yt_search_or_link: Optional[str]):
        # send message in discord chat
        await ctx.send('Play!')
        # try:
        #     # no "url" provided
        #     if yt_search_or_link == None:
        #         await ctx.send('Please provide a YouTube link or YouTube search info! :pleading_face:')
        #     else:
        #         # if "url" is not a real url link, then "YoutubeSearch" and create new a YouTube url link
        #         if 'www.youtube.com' not in yt_search_or_link:
        #             yt = YoutubeSearch(yt_search_or_link, max_results=1).to_json()
        #             yt_id = str(json.loads(yt)['videos'][0]['id'])
        #             yt_search_or_link = 'https://www.youtube.com/watch?v=' + yt_id

        #         # append "url_link" to "yt_links" file
        #         add_yt_links_file = open("resource_files/music_bot_files/yt_links.txt", "a")
        #         add_yt_links_file.write('\n' + yt_search_or_link)
        #         add_yt_links_file.close()
        #         open_yt_links_file = open("resource_files/music_bot_files/yt_links.txt")

        #         # get_url function
        #         url = get_url()

        #         # check if bot is in channel and join if is not
        #         channel = ctx.message.author.voice.channel
        #         if channel:
        #             voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        #             if voice and voice.is_connected():
        #                 await voice.move_to(channel)
        #             else:
        #                 voice = await channel.connect()

        #             # audio not playing then play audio
        #             if not voice.is_playing():
        #                 await ctx.send(':musical_note: BeeBot will now bee playing ***{}!*** '
        #                             ':musical_note:'.format(message_now_playing(url)))
        #                 # call "download_song" function
        #                 download_song(ctx)
        #                 # already seen in "download_song()" function
        #                 # voice.play(discord.FFmpegPCMAudio("resource_files/music_bot_files/song.mp3"),
        #                 # after=lambda e: download_song(ctx))
        #                 # voice.is_playing()
        #             else:
        #                 # if music is audio is playing already, add audio to queue
        #                 await ctx.send(':musical_note: Your audio has been added to the queue! :smile:')
        # except:
        #     print("Ignoring errors.")

def setup(bot):
    bot.add_cog(play(bot))