from discord.ext import commands

from ..models import Game
from . import generic_cog_mixin


class RocketLeagueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def rl(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    @rl.command()
    async def help(self, ctx):
        await generic_cog_mixin.help(ctx, Game.ROCKETLEAGUE)

    @rl.command()
    async def id(self, ctx, game_id: str):
        await generic_cog_mixin.register_player(ctx, Game.ROCKETLEAGUE, game_id)

    @rl.command()
    async def play(self, ctx):
        await generic_cog_mixin.join_queue(ctx, Game.ROCKETLEAGUE)

    @rl.command()
    async def leave(self, ctx):
        await generic_cog_mixin.leave_queue(ctx, Game.ROCKETLEAGUE)

    @rl.command()
    async def queue(self, ctx):
        await generic_cog_mixin.get_queue(ctx, Game.ROCKETLEAGUE)

    @rl.command()
    @commands.has_role("admin")
    async def pop(self, ctx, count: int = 5):
        await generic_cog_mixin.play(ctx, Game.ROCKETLEAGUE, count)
