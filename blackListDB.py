import copy
import re

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from typing import Union

import config
from log import Log
from playerData import PlayerData

NAME_FIELD = "name"
BLOCK_GAME_FIELD = "block_game"
DESCRIPTION_FIELD = "description"


class BlackListDatabase:
    @staticmethod
    def init_database():
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("BlackList.db")

        if not db.open():
            Log.save_log("Невозможно открыть базу данных")
            return

        query = QSqlQuery()
        query.exec(
            f"CREATE TABLE IF NOT EXISTS {config.TABLE_NAME} "
            f"(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            f"{NAME_FIELD} TEXT, "
            f"{BLOCK_GAME_FIELD} INT, "
            f"{DESCRIPTION_FIELD} TEXT)"
        )

    @staticmethod
    def update_player(player: PlayerData):
        query = QSqlQuery()
        query.exec(f"UPDATE {config.TABLE_NAME} SET "
                   f"{BLOCK_GAME_FIELD} = '{player.block_game}', "
                   f"{DESCRIPTION_FIELD} = '{player.description}' "
                   f"WHERE LOWER({NAME_FIELD}) = '{player.name.lower()}'")

    @staticmethod
    def insert_player(player: PlayerData):
        query = QSqlQuery()
        query.exec(f"INSERT INTO {config.TABLE_NAME} "
                   f"({NAME_FIELD}, {BLOCK_GAME_FIELD}, {DESCRIPTION_FIELD}) "
                   f"VALUES ('{player.name}', '{player.block_game}', '{player.description}')")

    @staticmethod
    def delete_player_by_name(player_name: str):
        query = QSqlQuery()
        query.exec(f"DELETE FROM {config.TABLE_NAME} "
                   f"WHERE LOWER({NAME_FIELD}) = '{player_name.lower()}'")

    @staticmethod
    def get_player_by_name(player_name: str) -> Union[PlayerData, None]:
        query = QSqlQuery()
        query.exec(f"SELECT * FROM {config.TABLE_NAME} "
                   f"WHERE LOWER({NAME_FIELD}) = '{player_name.lower()}'")

        if query.next():
            name = query.record().value(NAME_FIELD)
            block_game = query.record().value(BLOCK_GAME_FIELD)
            description = query.record().value(DESCRIPTION_FIELD)
            return PlayerData(name=name, block_game=block_game, description=description)
        else:
            return None

    @staticmethod
    def find_players_by_name(players_name: list[str]) -> list[PlayerData]:
        players = BlackListDatabase.get_all_players(is_sorted=True)
        filtered_players_dict = {}

        for key, value in config.IDENTICAL_CHARACTERS.items():
            for i in range(len(players_name)):
                players_name[i] = re.sub(re.escape(key), value, players_name[i].lower())

        players_edited = copy.deepcopy(players)
        for key, value in config.IDENTICAL_CHARACTERS.items():
            for i in range(len(players_edited)):
                players_edited[i].name = re.sub(re.escape(key), value, players_edited[i].name.lower())

        for i in range(len(players_edited)):
            for name in players_name:
                if config.MAXIMUM_NICKNAME_COMPARE < 0:
                    if players_edited[i].name.lower() == name.lower():
                        filtered_players_dict[players_edited[i].name] = players[i]
                else:
                    if players_edited[i].name[:config.MAXIMUM_NICKNAME_COMPARE].lower() == name[:config.MAXIMUM_NICKNAME_COMPARE].lower():
                        filtered_players_dict[players_edited[i].name] = players[i]

        return list(filtered_players_dict.values())

    @staticmethod
    def new_game():
        QSqlQuery(f"UPDATE {config.TABLE_NAME} "
                  f"SET {BLOCK_GAME_FIELD} = {BLOCK_GAME_FIELD} - 1 "
                  f"WHERE {BLOCK_GAME_FIELD} > 0")

    @staticmethod
    def get_all_players(is_sorted: bool) -> list[PlayerData]:
        query = QSqlQuery(f"SELECT * FROM {config.TABLE_NAME}")

        players = []
        while query.next():
            name = query.record().value(NAME_FIELD)
            block_game = query.record().value(BLOCK_GAME_FIELD)
            description = query.record().value(DESCRIPTION_FIELD)

            player = PlayerData(name=name, block_game=block_game, description=description)
            players.append(player)

        if is_sorted:
            return sorted(players, key=lambda x: x.block_game, reverse=True)
        else:
            return players
