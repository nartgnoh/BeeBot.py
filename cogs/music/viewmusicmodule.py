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
    @commands.command(name='viewcurrent', aliases=['currentview', 'currentaudio', 'vcurrent', 'cview', 'current'],
                      help='🎵 View the current audio!')
    async def view_current(self, ctx):
        if not music_helper.check_song_list():
            await ctx.send("There's no current audio! :open_mouth: Add a song with the \"play\" command! :smile:")
        else:
            current_song = music_helper.get_current_song()
            # *********
            # | embed |
            # *********
            embed = Embed(title="🎵 Current Song 🎵",
                          description=f"{current_song['title']} [duration: 00:00/{current_song['duration']}]",
                          colour=ctx.author.colour)
            # embed thumbnail
            thumb_url = current_song['thumbnails'][0]
            embed.set_thumbnail(url=thumb_url)
            await ctx.send(embed=embed)

        # get the length of song.mp3
        song_mp3_path = "/".join(list(current_directory.split('/')
                                   [0:-2])) + '/resource_files/music_files/games.json'
        # get games.json file
        games_json_path = "/".join(list(current_directory.split('/')
                                   [0:-2])) + '/resource_files/json_files/games.json'
        song_length = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                      'default=noprint_wrappers=1:nokey=1', song_file], stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
        song_seconds = int(float(song_length.stdout))
        song_time = time.gmtime(song_seconds)
        song_duration = str(time.strftime("%H:%M:%S", song_time))
        if song_duration[:2] == "00":
            song_duration = song_duration[3:]

        # # get name of song
        # yt_current_file = open("resource_files/music_bot_files/yt_current.txt")
        # read_file = yt_current_file.readline()
        # message = message_now_playing(read_file)
        # await ctx.send(':musical_note:  BeeBot is currently playing ***{} (Duration: {})!*** '
        #             ':musical_note:'.format(message, song_duration))
        # await ctx.send("There's no current audio! :open_mouth:")

    # # bot command to view next audio
    # @commands.command(name='viewnext', aliases=['nextview', 'nextaudio', 'vnext', 'nview'],
    #             help='🎶 View the next audio!')
    # async def view_next(self, ctx):
    #     try:
    #         key = 0
    #         next_yt_links_file = open("resource_files/music_bot_files/yt_links.txt")
    #         # read first line
    #         first_line = open('resource_files/music_bot_files/yt_links.txt').readlines()
    #         # delete if it is a "\n"
    #         if first_line[key] == '\n':
    #             lines = open('resource_files/music_bot_files/yt_links.txt').readlines()
    #             with open('resource_files/music_bot_files/yt_links.txt', 'w') as f:
    #                 f.writelines(lines[1:])
    #         next_yt_links_file.flush()
    #         first_line = open('resource_files/music_bot_files/yt_links.txt').readlines()
    #         # send message
    #         message = message_now_playing(first_line[key])
    #         await ctx.send(':musical_note:  BeeBot will be ***{}*** next!'
    #                     ':musical_note:'.format(message))
    #     except:
    #         await ctx.send("There's no next audio! :open_mouth:")

    # # bot command to view current queue
    # @commands.command(name='viewqueue', aliases=['queueview', 'currentqueue', 'viewq', 'qview', 'queue'],
    #             help='🎼 View the current queue!')
    # async def current_queue(self, ctx):
    #     # order of use
    #     new_yt_links_file = open("resource_files/music_bot_files/yt_links.txt")
    #     new_yt_links_file.flush()
    #     count = 0
    #     title_count = 0
    #     queue_array = []
    #     title_array = []
    #     queue_array_num = []
    #     final_message = ''
    #     try:
    #         voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #         if not voice.is_playing:
    #             await ctx.send('There is not audio in the queue! :flushed: Try the "play" command to add a song! :smile:')
    #         else:
    #             # transfer file elements to "queue_array"
    #             for lines in new_yt_links_file:
    #                 lines = lines.rstrip()
    #                 queue_array.append(lines)
    #                 count += 1

    #             # check if "yt_links.txt" is empty
    #             fl_check = Path(r'{}/resource_files/music_bot_files/yt_links.txt'.format(parent_dir))
    #             if not fl_check.stat().st_size == 0:
    #                 # pop initial "\n"
    #                 fl_check = open('resource_files/music_bot_files/yt_links.txt').readlines()
    #                 if fl_check[0] == '\n' or fl_check[0] == '':
    #                     queue_array.pop(0)
    #             # add current song
    #             if voice.is_playing:
    #                 yt_current_file = open("resource_files/music_bot_files/yt_current.txt")
    #                 yt_current_file.flush()
    #                 current_audio = yt_current_file.readline()
    #                 queue_array.insert(0, current_audio)
    #             # create an array of "titles"
    #             for url in queue_array:
    #                 # call the "message_now_playing" function to get YouTube titles
    #                 url_title = message_now_playing(url)

    #                 titles = [url_title]
    #                 title_array.append(titles)
    #             # create array of formatted elements (Example: "1 : 'current song'")
    #             for key in title_array:
    #                 title_count += 1
    #                 new_array_line = '{} : {}\n'.format(title_count, str(key)[1:-1])
    #                 queue_array_num.append(new_array_line)
    #             # create a single final_message string
    #             for key in queue_array_num:
    #                 final_message += key
    #             # send queue message
    #             await ctx.send(':musical_note: :musical_note:  The current queue is: :musical_note: :musical_note:'
    #                         '\n{}'.format(final_message))
    #     except:
    #         # errors
    #         await ctx.send('There is not audio in the queue! :flushed: Try the \"play\" command to add a song! :smile:')


def setup(bot):
    bot.add_cog(viewmusicmodule(bot))
