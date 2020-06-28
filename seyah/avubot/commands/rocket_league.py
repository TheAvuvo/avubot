import sqlite3
from typing import Optional, List

import aiosqlite

from ..models import GameUser


QUEUE_INSERT = "INSERT INTO queue (discord, twitch, game_id) VALUES (?, ?, ?);"
QUEUE_DELETE = ("DELETE FROM queue WHERE (discord IS NULL OR discord LIKE ?) "
                "AND (twitch IS NULL OR twitch LIKE ?);")
QUEUE_GET = "SELECT * FROM queue ORDER BY id LIMIT ?;"
QUEUE_POP = "DELETE FROM queue WHERE id IN (SELECT id FROM queue ORDER BY id LIMIT ?);"


async def add_to_queue(discord: Optional[str],
                       twitch: Optional[str],
                       game_id: Optional[str]) -> int:
    try:
        async with aiosqlite.connect("avubot.db") as db:
            await db.execute(QUEUE_INSERT, (discord, twitch, game_id))
            await db.commit()
            return True
    except aiosqlite.IntegrityError:
        return False


async def drop_from_queue(discord: Optional[str], twitch: Optional[str]) -> bool:
    async with aiosqlite.connect("avubot.db") as db:
        async with db.execute(QUEUE_DELETE, (discord, twitch)) as cursor:
            await db.commit()
            return cursor.rowcount > 0


async def pop_from_queue(count: int) -> List[GameUser]:
    game_users: List[GameUser] = []
    async with aiosqlite.connect("avubot.db") as db:
        async with db.execute(QUEUE_GET, (count, )) as cursor:
            async for row in cursor:
                game_users.append(GameUser(id=row[0],
                                           discord=row[1],
                                           twitch=row[2],
                                           game_id=row[3]))
        async with db.execute(QUEUE_POP, (count, )) as cursor:
            await db.commit()
    return game_users


async def get_queue() -> List[GameUser]:
    game_users: List[GameUser] = []
    async with aiosqlite.connect("avubot.db") as db:
        async with db.execute(QUEUE_GET, (8, )) as cursor:
            async for row in cursor:
                game_users.append(GameUser(id=row[0],
                                           discord=row[1],
                                           twitch=row[2],
                                           game_id=row[3]))
    return game_users


def create_table():
    with sqlite3.connect("avubot.db") as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id integer PRIMARY KEY AUTOINCREMENT,
                discord text UNIQUE,
                twitch text UNIQUE,
                game_id text
            );""")
