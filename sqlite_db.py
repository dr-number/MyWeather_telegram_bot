from re import I
import sqlite3
from sqlite3 import Cursor

class Sqlite3DB():

    __conn = None
    __cursor = None

    def connect_db(self):
        self.__conn = sqlite3.connect('bot.db', check_same_thread=False)
        self.__cursor = self.__conn.cursor()

    def create_user(self, chat_id: int):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            name_city TEXT default '',
            lon REAL default 0.0,
            lat REAL default 0.0);
            """)

        user = (str(chat_id))

        self.__cursor.execute("INSERT INTO users VALUES(?);", user)
        self.__conn.commit()

        