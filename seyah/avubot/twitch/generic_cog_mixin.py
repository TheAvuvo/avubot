import textwrap
from typing import List, Optional

from ..commands import generic
from ..models import Game, GameUser, Platform


async def help(ctx, game: Game):
    cm = game.cmd()
    help_msg = (f"```\n"
                f"Commands for joining {str(game)} in-house games:\n\n"
                f"* !{cm} play <gametag> - Join the queue for in-house games\n"
                f"* !{cm} leave - Leave the queue for in-house games"
                "```")
    await ctx.send(textwrap.dedent(help_msg))


async def register_player(ctx, game: Game, game_id: str):
    await generic.register_player(uid=ctx.author.id,
                                  username=ctx.author.name,
                                  platform=Platform.TWITCH,
                                  game=game,
                                  game_id=game_id)
    await ctx.send(f"Registered @{ctx.author.display_name} as {game_id} "
                   f"({game})")


async def join_queue(ctx, game: Game, game_id: Optional[str]):
    if game_id is not None:
        await register_player(ctx, game, game_id)

    queue_position: int = await generic.join_queue(uid=ctx.author.id,
                                                   platform=Platform.TWITCH,
                                                   game=game)
    if queue_position >= 0:
        await ctx.send(f"Queuing @{ctx.author.display_name} "
                       f"(Position: #{queue_position})")
    elif queue_position == -2:
        await ctx.send(f"@{ctx.author.display_name} not registered yet!")
    else:
        await ctx.send(f"@{ctx.author.display_name} already queued!")


async def leave_queue(ctx, game: Game):
    status: bool = await generic.leave_queue(uid=ctx.author.id, game=game)
    if status:
        await ctx.send(f"@{ctx.author.display_name} left the queue")


async def get_queue(ctx, game: Game):
    game_users: List[GameUser] = await generic.get_queue(game=game)
    if len(game_users) <= 0:
        await ctx.send("No one has entered the queue!")
        return
    output = "QUEUE:     "
    for index, game_user in enumerate(game_users):
        output += f"#{index + 1} {game_user.username} [{game_user.game_id}]; "
    await ctx.send(output)


async def play(ctx, game: Game, count: int):
    game_users: List[GameUser] = await generic.pop_queue(game=game, count=count)
    if len(game_users) <= 0:
        await ctx.send("No one has entered the queue!")
        return
    output = "PLAYING NOW:     "
    for index, game_user in enumerate(game_users):
        output += f"#{index + 1} {game_user.username} [{game_user.game_id}]; "
    await ctx.send(output)
