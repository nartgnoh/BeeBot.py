# *********************************************************************************************************************
# reactions_listener.py
# *********************************************************************************************************************

import cogs.helper.helper_functions.events as events

from discord.ext.commands import Cog


class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # listener for on_raw_reaction_add
    # *********************************************************************************************************************
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # ***********************************
        # | delete message on '❌' reaction |
        # ***********************************
        if payload.emoji.name == '❌' and payload.member != self.bot.user:
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            first_reaction_users = await message.reactions[0].users().flatten()
            if self.bot.user in first_reaction_users and len(first_reaction_users) > 1:
                await message.delete()

        # *********************************
        # | add participants to giveaways |
        # *********************************
        if payload.member != self.bot.user:
            events_data = events.get_events_json()
            if 'giveaways' in events_data:
                if str(payload.message_id) in events_data['giveaways']:
                    giveaway = events_data['giveaways'][str(
                        payload.message_id)]
                    if payload.emoji.name == giveaway['reaction'] and not str(payload.member.id) in giveaway['participants']:
                        giveaway['participants'][str(payload.member.id)] = str(
                            payload.member.display_name)
                        events.set_events_json(events_data)

    # *********************************************************************************************************************
    # listener for on_raw_reaction_remove
    # *********************************************************************************************************************
    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # ************************************
        # | remove participants to giveaways |
        # ************************************
        events_data = events.get_events_json()
        if 'giveaways' in events_data:
            if str(payload.message_id) in events_data['giveaways']:
                giveaway = events_data['giveaways'][str(
                    payload.message_id)]
                if payload.emoji.name == giveaway['reaction'] and str(payload.user_id) in giveaway['participants']:
                    giveaway['participants'].pop(str(payload.user_id))
                    events.set_events_json(events_data)


def setup(bot):
    bot.add_cog(Reactions(bot))
