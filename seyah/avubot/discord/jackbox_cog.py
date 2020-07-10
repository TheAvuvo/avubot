from typing import Optional

from discord.ext import commands

from ..models import Game
from . import generic_cog_mixin


class JackboxCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def jackbox(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    @jackbox.command()
    async def help(self, ctx):
        await generic_cog_mixin.help(ctx, Game.JACKBOX)

    @jackbox.command()
    async def id(self, ctx, game_id: str):
        await generic_cog_mixin.register_player(ctx, Game.JACKBOX, game_id)

    @jackbox.command()
    async def play(self, ctx, game_id: Optional[str]):
        await generic_cog_mixin.join_queue(ctx, Game.JACKBOX, game_id)

    @jackbox.command()
    async def leave(self, ctx):
        await generic_cog_mixin.leave_queue(ctx, Game.JACKBOX)

    @jackbox.command()
    async def queue(self, ctx):
        await generic_cog_mixin.get_queue(ctx, Game.JACKBOX)

    @jackbox.command()
    @commands.has_role("admin")
    async def pop(self, ctx, count: int = 5):
        await generic_cog_mixin.play(ctx, Game.JACKBOX, count)
