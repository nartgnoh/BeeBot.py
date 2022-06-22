# # *********************************************************************************************************************
# # voice_states_listener.py
# # *********************************************************************************************************************

# from discord.ext.commands import Cog


# class Voice_State(Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     # *********************************************************************************************************************
#     # listener for on_voice_state_update
#     # *********************************************************************************************************************
#     @Cog.listener()
#     async def on_voice_state_update(self, member, before, after):
#         print("sees every voice state change (both disconnect and connects)")

# def setup(bot):
#     bot.add_cog(Voice_State(bot))
