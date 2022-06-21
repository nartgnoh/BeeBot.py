# *********************************************************************************************************************
# playmusicmodule.py
# - (wip)
# *********************************************************************************************************************

import os
import discord
import random

from discord.ext import commands
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# playmusicmodule class


class playmusicmodule(commands.Cog, name="PlayMusicModule", description=""):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to join voice channel
    # *********************************************************************************************************************
    @commands.command(name='join', aliases=['joincall', '🔊'], help='🔊 Beebot joins your voice channel!')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Why am I here? :slight_smile:\nIf you want to play music, use the \"play\" command! :smile:")

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

    # *********************************************************************************************************************
    # bot command to play Youtube Audio
    # *********************************************************************************************************************
    @commands.command(name='play', aliases=['playaudio', 'playsong'],
                      help='▶️ Plays YouTube audio! Provide YouTube search or link! [Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def play(self, ctx, *, yt_search_or_link: Optional[str]):
        if yt_search_or_link == None:
            await ctx.send('Please provide a YouTube link or YouTube search info! :pleading_face:')
        else:
            # get_url function
            url = get_url()

            # check if bot is in channel and join if is not
            channel = ctx.message.author.voice.channel
            if channel:
                voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()

                # audio not playing then play audio
                if not voice.is_playing():
                    await ctx.send(':musical_note: BeeBot will now bee playing ***{}!*** '
                                   ':musical_note:'.format(message_now_playing(url)))
                    # call "download_song" function
                    download_song(ctx)
                    # already seen in "download_song()" function
                    # voice.play(discord.FFmpegPCMAudio("resource_files/music_bot_files/song.mp3"),
                    # after=lambda e: download_song(ctx))
                    # voice.is_playing()
                else:
                    # if music is audio is playing already, add audio to queue
                    await ctx.send(':musical_note: Your audio has been added to the queue! :smile:')



# bot command to go to next audio in queue by reaction vote
@bot.command(name='next', aliases=['skip'], help='⏭️ Play the next audio! (Role specific) ♫')
# only specific roles can use this command
@commands.has_role(role_specific_command_name)
async def next(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        # check if the queue is empty
        fl_check = Path(r'{}/resource_files/music_bot_files/yt_links.txt'.format(parent_dir))
        if not fl_check.stat().st_size == 0:
            # check if voice is playing
            if not voice.is_playing:
                await ctx.send('Not playing any music right now. :thinking:')
            else:
                # get url for message
                url = get_url()
                await ctx.send(':musical_note: BeeBot will now bee playing ***{}!*** '
                               ':musical_note:'.format(message_now_playing(url)))
                # stop the current song
                voice.stop()
                # download "next_song.mp3" and play that
                download_next_song(ctx)
        else:
            await ctx.send(
                "There is not more audio in the queue! :flushed: Try the \"play\" command to add a song! :smile:")
    except:
        await ctx.send("An error has occurred! :open_mouth: Please try again!")


# bot command to pause audio
@bot.command(name='pause', aliases=['pauseaudio'], help='⏸️ Pause current audio playing! (Role specific) ♫')
# only specific roles can use this command
@commands.has_role(role_specific_command_name)
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send("Pausing audio! :pause_button:")
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing. :thinking:")


# bot command to resume audio
@bot.command(name='resume', aliases=['resumeaudio'], help='⏯️ Resume current audio playing! (Role specific) ♫')
# only specific roles can use this command
@commands.has_role(role_specific_command_name)
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await ctx.send("Resuming audio! :headphones:")
        voice.resume()
    else:
        await ctx.send("The audio is not paused. :thinking:")



def setup(bot):
    bot.add_cog(playmusicmodule(bot))
