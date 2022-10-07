import sqlite3
from sqlite3 import Cursor

class Sqlite3DB:

    __conn = None
    __cursor = None

    def connect_db(self) -> Cursor:
        self.__conn = sqlite3.connect('bot.db')
        self.__cursor = self.__conn.cursor()
        return self.__cursor