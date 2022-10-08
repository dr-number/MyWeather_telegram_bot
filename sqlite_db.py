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
            description TEXT default '',
            lon REAL default 0.0,
            lat REAL default 0.0);
            """)

        if self.is_exist_user(chat_id):
            self.__cursor.execute("INSERT INTO users(chat_id) VALUES(?);", (chat_id,))
            self.__conn.commit()

    
    def is_exist_user(self, chat_id: int):
        self.__cursor.execute("SELECT chat_id FROM users WHERE chat_id = ?", (chat_id,))
        return self.__cursor.fetchone() is None


    def get_user(self, chat_id: int) -> set:
        self.__cursor.execute("SELECT description, lon, lat FROM users WHERE chat_id = ?", (chat_id,))
        data = self.__cursor.fetchone()

        if data:
            return {
                "description": data[0],
                "lon": data[1],
                "lat": data[2]
            }
        
        return {}


    def update_city(self, chat_id: int, lon: float, lat: float, description: str = ''):
        self.__cursor.execute(f"UPDATE users SET description = ?, lon = ?, lat = ? WHERE chat_id= ?;", (description, lon, lat, chat_id))
        self.__conn.commit()


        