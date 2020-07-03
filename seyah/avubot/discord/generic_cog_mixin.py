import textwrap
from typing import List

from discord import Embed

from ..commands import generic
from ..models import Game, GameUser, Platform


async def help(ctx, game: Game):
    cm = game.cmd()
    help_msg = (f"```\n"
                f"Commands for joining {str(game)} in-house games:\n\n"
                f"* !{cm} id <gametag> - Register your gametag. "
                "E.g. EarlGrey#1234.\n\n"
                f"* !{cm} play  - Join the queue for in-house games\n"
                f"* !{cm} leave - Leave the queue for in-house games"
                "```")
    await ctx.send(textwrap.dedent(help_msg))


async def register_player(ctx, game: Game, game_id: str):
    await generic.register_player(uid=ctx.author.id,
                                  username=ctx.author.name,
                                  platform=Platform.DISCORD,
                                  game=game,
                                  game_id=game_id)
    await ctx.send(f"Registered {ctx.author.mention} as {game_id} "
                   f"({game})")


async def join_queue(ctx, game: Game):
    queue_position: int = await generic.join_queue(uid=ctx.author.id,
                                                   platform=Platform.DISCORD,
                                                   game=game)
    if queue_position >= 0:
        await ctx.send(f"Queuing {ctx.author.mention} (Position: #{queue_position})")
    elif queue_position == -2:
        await ctx.send(f"{ctx.author.mention} not registered yet!")
    else:
        await ctx.send(f"{ctx.author.mention} already queued!")


async def leave_queue(ctx, game: Game):
    status: bool = await generic.leave_queue(uid=ctx.author.id, game=game)
    if status:
        await ctx.send(f"{ctx.author.display_name} left the queue")


async def get_queue(ctx, game: Game):
    game_users: List[GameUser] = await generic.get_queue(game=game)
    if len(game_users) <= 0:
        await ctx.send("No one has entered the queue!")
        return

    embed = Embed(title="In Queue", color=0x00ffff)
    for index, game_user in enumerate(game_users):
        embed.add_field(name=(f"{index + 1}: {game_user.username} "
                              f"[{str(game_user.platform).lower()}]"),
                        value=f"{game_user.game_id}",
                        inline=False)
    await ctx.send(embed=embed)


async def play(ctx, game: Game, count: int):
    game_users: List[GameUser] = await generic.pop_queue(game=game, count=count)
    if len(game_users) <= 0:
        await ctx.send("No one has entered the queue!")
        return

    embed = Embed(title="Playing Now", color=0x00ff00)
    for index, game_user in enumerate(game_users):
        embed.add_field(name=(f"{index + 1}: {game_user.username} "
                              f"[{str(game_user.platform).lower()}]"),
                        value=f"{game_user.game_id}",
                        inline=True)
    await ctx.send(embed=embed)
