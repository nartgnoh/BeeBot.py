# *********************************************************************************************************************
# playmusicmodule.py
# - play
# - leave
# *********************************************************************************************************************

from dis import disco
import os
import discord
import cogs.helper.helper_functions.music as music_helper

from discord.ext import commands
from discord.voice_client import VoiceClient
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# playmusicmodule class


class playmusicmodule(commands.Cog, name="PlayMusicModule", description="BeeBot's Music Bot! Type \"BB help PlayMusicModule\" for options!"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to play Youtube Audio
    # *********************************************************************************************************************
    @commands.command(name='play', aliases=['playaudio', 'playsong', '▶️'],
                      help='▶️ Plays YouTube audio! Provide YouTube search or link! [Max length: 15mins, Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def play(self, ctx, *, yt_search_or_link: Optional[str]):
        if yt_search_or_link == None:
            await ctx.send('Please provide a YouTube link or YouTube search info! :pleading_face:')
        else:
            if ctx.author.voice is None:
                await ctx.send('Please join a discord channel to use this command! :slight_smile:')
            else:
                check = music_helper.add_url(yt_search_or_link)
                if not check:
                    await ctx.send('Sorry! The song you were trying to play is too long! :cry: [Max length: 15mins]')
                else:
                    channel = ctx.message.author.voice.channel
                    voice = ctx.voice_client
                    if voice is None:
                        await channel.connect()
                    else:
                        await voice.move_to(channel)
                    voice = ctx.voice_client
                    print("---------------- PLAY ----------------")
                    print(voice)
                    if voice.is_playing():
                        # *********
                        # | embed |
                        # *********
                        embed = Embed(title=f"{check['title']}\n🎶 Added to Queue! 🎶",
                                      colour=ctx.author.colour)
                        await ctx.send(embed=embed)
                    else:
                        current_song = music_helper.get_current_song()
                        music_helper.play_music(self, ctx)
                        # *********
                        # | embed |
                        # *********
                        embed = Embed(title=f"🎵 Now Playing 🎵\n{current_song['title']}",
                                      description=f"By: {current_song['channel']}\nDuration: {current_song['duration']}",
                                      colour=ctx.author.colour)
                        # embed thumbnail
                        thumb_url = current_song['thumbnails'][0]
                        embed.set_thumbnail(url=thumb_url)
                        await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to go to next audio in queue by reaction vote
    # *********************************************************************************************************************
    @commands.command(name='next', aliases=['skip', '⏭️'], help='⏭️ Play the next audio! [Role specific] ♫')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def next(self, ctx):
        voice = ctx.voice_client
        if ctx.author.voice is None:
            await ctx.send('Please join a discord channel to use this command! :slight_smile:')
        else:
            songs_list = music_helper.get_songs_list()
            if not len(songs_list) > 1:
                await ctx.send("There is not more audio in the queue! :flushed: Try the \"play\" command to add a song! :smile:")
            else:
                if not voice.is_playing():
                    await ctx.send('Not playing any music right now. :thinking: Try the \"play\" command to add a song! :smile:')
                else:
                    next_song = music_helper.get_next_song
                    voice.stop()
                    music_helper.play_next(self, ctx)
                    # *********
                    # | embed |
                    # *********
                    embed = Embed(title=f"🎵 [Next] Now Playing 🎵\n{next_song['title']}",
                                  description=f"By: {next_song['channel']}\nDuration: {next_song['duration']}",
                                  colour=ctx.author.colour)
                    # embed thumbnail
                    thumb_url = next_song['thumbnails'][0]
                    embed.set_thumbnail(url=thumb_url)
                    await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to pause audio
    # *********************************************************************************************************************
    @commands.command(name='pause', aliases=['pauseaudio', '⏸️'], help='⏸️ Pause current audio playing! [Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def pause(self, ctx):
        try:
            voice = ctx.voice_client
            if voice.is_playing():
                await ctx.send("Pausing audio! :pause_button:")
                voice.pause()
        except:
            await ctx.send("Currently no audio is playing. :thinking:")

    # *********************************************************************************************************************
    # bot command to resume audio
    # *********************************************************************************************************************
    @commands.command(name='resume', aliases=['resumeaudio', '⏯️'], help='⏯️ Resume current audio playing! [Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def resume(self, ctx):
        try:
            voice = ctx.voice_client
            if voice.is_paused():
                await ctx.send("Resuming audio! :headphones:")
                voice.resume()
        except:
            await ctx.send("The audio is not paused. :thinking:")

    # *********************************************************************************************************************
    # bot command to leave voice channel and deletes queue
    # *********************************************************************************************************************
    @commands.command(name='leave', aliases=['stopaudio', 'leavecall', 'deletequeue', 'disconnect', '🔈'],
                      help='🔈 Beebot leaves voice channel and deletes current queue. [Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def leave(self, ctx):
        try:
            voice = ctx.voice_client
            if voice.is_connected():
                voice.stop()
                music_helper.reset_songs_list()
                await voice.disconnect()
                await ctx.send("Ok I'll leave. :cry:")
        except:
            await ctx.send("BeeBot is not connected to a voice channel. :thinking:")


def setup(bot):
    bot.add_cog(playmusicmodule(bot))
