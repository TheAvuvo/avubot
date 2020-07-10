from twitchio.ext import commands

from ..models import Game
from . import generic_cog_mixin


class RocketLeagueCog(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    def is_mod(self, ctx):
        return ctx.message.author.is_mod == 1

    @commands.command(name="rlhelp")
    async def help(self, ctx):
        await generic_cog_mixin.help(ctx, Game.ROCKETLEAGUE)

    @commands.command(name="rlplay")
    async def play(self, ctx, game_id: str):
        await generic_cog_mixin.join_queue(ctx, Game.ROCKETLEAGUE, game_id)

    @commands.command(name="rlleave")
    async def leave(self, ctx):
        await generic_cog_mixin.leave_queue(ctx, Game.ROCKETLEAGUE)

    @commands.command(name="rlqueue")
    async def queue(self, ctx):
        await generic_cog_mixin.get_queue(ctx, Game.ROCKETLEAGUE)

    @commands.command(name="rlpop")
    async def pop(self, ctx, count: int = 5):
        if not self.is_mod(ctx):
            return
        await generic_cog_mixin.play(ctx, Game.ROCKETLEAGUE, count)
