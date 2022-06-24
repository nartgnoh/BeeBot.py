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
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        first_reaction_users = await message.reactions[0].users().flatten()

        # ***********************************
        # | delete message on '❌' reaction |
        # ***********************************
        for u in first_reaction_users:
            if u.bot and len(first_reaction_users) > 1 and payload.emoji.name == '❌':
                await message.delete()
                break

        # *********************************
        # | add participants to giveaways |
        # *********************************
        if len(first_reaction_users) > 1:
            events_data = events.get_events_json()
            if 'giveaways' in events_data:
                if str(payload.message_id) in events_data['giveaways']:
                    giveaway = events_data['giveaways'][str(payload.message_id)]
                    if payload.emoji.name == giveaway['reaction']:
                        giveaway['participants'][int(payload.member.id)] = str(payload.member.display_name)
                        events.set_events_json(events_data)


def setup(bot):
    bot.add_cog(Reactions(bot))
