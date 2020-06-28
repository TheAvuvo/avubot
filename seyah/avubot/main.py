import os

from dotenv import load_dotenv

from .discord.discord_integration import DiscordBot
from .twitch.twitch_integration import TwitchBot, TwitchCog
from .discord.rl_cog import RLAdaptor


load_dotenv()


if __name__ == "__main__":
    discord_bot = DiscordBot(command_prefix="!")
    discord_bot.add_cog(RLAdaptor(discord_bot))
    discord_bot.add_cog(TwitchCog(discord_bot, TwitchBot()))
    discord_bot.run(os.environ["DISCORD_TOKEN"])
