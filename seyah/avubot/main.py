import os

from dotenv import load_dotenv

from .discord.bot import DiscordBot
# from .twitch.bot import TwitchBot, TwitchCog
from .discord import rocketleague_cog, valorant_cog, jackbox_cog
from .commands.generic import create_tables


load_dotenv()


if __name__ == "__main__":
    create_tables()
    discord_bot = DiscordBot(command_prefix="!")
    discord_bot.add_cog(rocketleague_cog.RocketLeagueCog(discord_bot))
    discord_bot.add_cog(valorant_cog.ValorantCog(discord_bot))
    discord_bot.add_cog(jackbox_cog.JackboxCog(discord_bot))
    # discord_bot.add_cog(TwitchCog(discord_bot, TwitchBot()))
    discord_bot.run(os.environ["DISCORD_TOKEN"])
