from discord import Embed
from discord.ext import commands


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
        await ctx.send(f"Queuing RL User {rl_id}. " +
                       f"Submitted by Discord user {ctx.author.display_name}")

    @rl.command()
    async def queue(self, ctx):
        embed = Embed(title="In-House Queue", color=0x00ff00)
        await ctx.send(embed=embed)
