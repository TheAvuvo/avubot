import os

from discord.ext import commands as discord_commands
from twitchio.ext import commands


class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.environ["TMI_TOKEN"],
                         client_id=os.environ["CLIENT_ID"],
                         nick=os.environ['BOT_NICK'],
                         prefix=os.environ['BOT_PREFIX'],
                         initial_channels=[os.environ['CHANNEL']])

        self.loop.create_task(self.start())

    # TwitchIO event
    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name="test")
    async def twitch_command(self, ctx):
        await ctx.send('Hai there!')


class TwitchCog(discord_commands.Cog):

    def __init__(self, discord_bot, twitch_bot):
        self.discord_bot = discord_bot
        self.twitch_bot = twitch_bot
