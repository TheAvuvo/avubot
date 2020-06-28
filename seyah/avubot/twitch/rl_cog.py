from typing import List

from twitchio.ext import commands

from ..commands import rocket_league
from ..models import GameUser


class RLAdaptor(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    def is_mod(self, ctx):
        return ctx.message.author.is_mod == 1

    @commands.command(name="rljoin")
    async def join(self, ctx, rl_id: str):
        display_name: str = ctx.author.name
        status: bool = await rocket_league.add_to_queue(discord=None,
                                                        twitch=display_name,
                                                        game_id=rl_id)
        if status:
            await ctx.send(f"Queuing {ctx.author.name}")
        else:
            await ctx.send(f"{ctx.author.name} already queued.")

    @commands.command(name="rlleave")
    async def leave(self, ctx):
        display_name: str = ctx.author.name
        status: bool = await rocket_league.drop_from_queue(discord=None,
                                                           twitch=display_name)
        if status:
            await ctx.send(f"{ctx.author.name} left the queue")

    @commands.command(name="rlqueue")
    async def queue(self, ctx):
        queue: List[GameUser] = await rocket_league.get_queue()
        description = ""
        for index, game_user in enumerate(queue):
            description += (f"#{index + 1}) {game_user.discord or game_user.twitch} "
                            f"(ID: {game_user.game_id})\r\n")
        await ctx.send(description)

    @commands.command(name="rlplay")
    async def pop(self, ctx, count: int = 5):
        if not self.is_mod(ctx):
            return

        game_users: List[GameUser] = await rocket_league.pop_from_queue(count=count)
        if len(game_users) <= 0:
            await ctx.send("No one has entered the queue!")

        description = "Next up! "
        for index, game_user in enumerate(game_users):
            description += (f"#{index + 1}) {game_user.discord or game_user.twitch} "
                            f"(ID: {game_user.game_id})\r\n")
        await ctx.send(description)
