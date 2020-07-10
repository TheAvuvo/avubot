import sqlite3
from typing import List, Optional

import aiosqlite

from ..models import Game, GameUser, Platform

USER_DB = "registrations.db"

CREATE_REGISTRATION = ("CREATE TABLE IF NOT EXISTS registration "
                       "(uid text, username text, platform text, game text, "
                       "game_id text, PRIMARY KEY (uid, game) ON CONFLICT REPLACE);")
CREATE_QUEUE = ("CREATE TABLE IF NOT EXISTS queue ("
                "id integer PRIMARY KEY AUTOINCREMENT, uid text, game text, "
                "UNIQUE(uid, game))")

REGISTRATION_INSERT = "INSERT INTO registration VALUES (?, ?, ?, ?, ?);"
REGISTRATION_GET = "SELECT * FROM registration WHERE uid=? AND platform=? AND game=?;"
QUEUE_INSERT = "INSERT INTO queue (uid, game) VALUES (?, ?);"
QUEUE_DELETE = "DELETE FROM queue WHERE uid=? AND game=?;"
QUEUE_GET = ("SELECT * FROM queue INNER JOIN registration users ON ("
             "users.uid = queue.uid AND users.game = queue.game) "
             "WHERE queue.game=? ORDER BY id LIMIT ?;")
QUEUE_POP = ("DELETE FROM queue WHERE id IN ("
             "SELECT id FROM queue WHERE game=? ORDER BY id LIMIT ?);")


async def register_player(uid: str,
                          username: str,
                          platform: Platform,
                          game: Game,
                          game_id: str):
    params_tuple = (uid, username, str(platform), str(game), game_id)
    async with aiosqlite.connect(USER_DB) as db:
        await db.execute(REGISTRATION_INSERT, params_tuple)
        await db.commit()


async def get_player(uid: str, platform: Platform, game: Game) -> Optional[GameUser]:
    async with aiosqlite.connect(USER_DB) as db:
        async with db.execute(REGISTRATION_GET, (uid, str(platform), str(game))) as c:
            async for row in c:
                game_user = GameUser(uid=row[0],
                                     username=row[1],
                                     platform=Platform(row[2]),
                                     game=Game.to_enum(row[3]),
                                     game_id=row[4])
                return game_user
    return None


async def join_queue(uid: str, platform: Platform, game: Game) -> int:
    game_user = await get_player(uid=uid, platform=platform, game=game)
    if game_user is None:
        return -2

    params_tuple = (uid, str(game))
    async with aiosqlite.connect(USER_DB) as db:
        try:
            await db.execute(QUEUE_INSERT, params_tuple)
            await db.commit()
        except sqlite3.IntegrityError:
            return -3

    users: List[GameUser] = await get_queue(game)
    queue_position = -1
    for index, user in enumerate(users):
        if user.uid == str(uid):
            queue_position = index + 1

    return queue_position


async def leave_queue(uid: str, game: Game) -> bool:
    params_tuple = (uid, str(game))
    async with aiosqlite.connect(USER_DB) as db:
        async with db.execute(QUEUE_DELETE, params_tuple) as cursor:
            await db.commit()
            return cursor.rowcount > 0


async def get_queue(game: Game) -> List[GameUser]:
    game_users: List[GameUser] = []
    params_tuple = (str(game), 100)
    async with aiosqlite.connect(USER_DB) as db:
        async with db.execute(QUEUE_GET, params_tuple) as cursor:
            async for row in cursor:
                game_users.append(GameUser(uid=row[1],
                                           username=row[4],
                                           platform=Platform(row[5]),
                                           game=Game.to_enum(row[6]),
                                           game_id=row[7]))
    return game_users


async def pop_queue(game: Game, count: int) -> List[GameUser]:
    game_users: List[GameUser] = []
    params_tuple = (str(game), count)
    async with aiosqlite.connect(USER_DB) as db:
        async with db.execute(QUEUE_GET, params_tuple) as cursor:
            async for row in cursor:
                game_users.append(GameUser(uid=row[1],
                                           username=row[4],
                                           platform=Platform(row[5]),
                                           game=Game.to_enum(row[6]),
                                           game_id=row[7]))
        await db.execute(QUEUE_POP, params_tuple)
        await db.commit()
    return game_users


def create_tables():
    with sqlite3.connect(USER_DB) as db:
        db.execute(CREATE_REGISTRATION)
        db.execute(CREATE_QUEUE)
