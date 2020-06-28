import os

from dotenv import load_dotenv

from .discord.bot import DiscordBot
from .twitch.bot import TwitchBot, TwitchCog
from .discord.rl_cog import RLAdaptor
from .commands.rocket_league import create_table as create_rocket_league_table


load_dotenv()


if __name__ == "__main__":
    create_rocket_league_table()
    discord_bot = DiscordBot(command_prefix="!")
    discord_bot.add_cog(RLAdaptor(discord_bot))
    discord_bot.add_cog(TwitchCog(discord_bot, TwitchBot()))
    discord_bot.run(os.environ["DISCORD_TOKEN"])
