from re import I
import sqlite3
from sqlite3 import Cursor

class Sqlite3DB():

    __conn = None
    __cursor = None

    def connect_db(self):
        self.__conn = sqlite3.connect('bot.db')
        self.__cursor = self.__conn.cursor()

    def create_user(self, chat_id: int):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY,
            chat_id int);
            """)

        user = ('00002', 'Lois', 'Lane', 'Female')

        