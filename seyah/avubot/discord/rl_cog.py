from typing import List

from discord import Embed
from discord.ext import commands

from ..commands import rocket_league
from ..models import GameUser


class RLAdaptor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def rl(self, ctx):
        """Gambles some money."""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    @rl.command()
    async def join(self, ctx, rl_id: str):
        display_name: str = ctx.author.display_name
        status: bool = await rocket_league.add_to_queue(discord=display_name,
                                                        twitch=None,
                                                        game_id=rl_id)

        if status:
            await ctx.send(f"Queuing {ctx.author.display_name}")
        else:
            await ctx.send(f"{ctx.author.display_name} already queued.")

    @rl.command()
    async def leave(self, ctx):
        display_name: str = ctx.author.display_name
        status: bool = await rocket_league.drop_from_queue(discord=display_name,
                                                           twitch=None)
        if status:
            await ctx.send(f"{ctx.author.display_name} left the queue")

    @rl.command()
    async def queue(self, ctx):
        queue: List[GameUser] = await rocket_league.get_queue()
        description = "```\n"
        for index, game_user in enumerate(queue):
            description += (f"{index + 1}) {game_user.discord or game_user.twitch} "
                            f"(ID: {game_user.game_id})\n")
        description += "```"
        embed = Embed(title="In-House Queue", description=description, color=0x0000ff)
        await ctx.send(embed=embed)

    @rl.command()
    @commands.has_role("admin")
    async def play(self, ctx, count: int = 5):
        game_users: List[GameUser] = await rocket_league.pop_from_queue(count=count)
        if len(game_users) <= 0:
            ctx.send("No one has entered the queue!")

        description = "```\n"
        for index, game_user in enumerate(game_users):
            description += (f"{index + 1}) {game_user.discord or game_user.twitch} "
                            f"(ID: {game_user.game_id})\n")
        description += "```"
        embed = Embed(title="Playing Now", description=description, color=0x00ff00)
        await ctx.send(embed=embed)
