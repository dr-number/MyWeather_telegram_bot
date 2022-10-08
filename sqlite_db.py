import sqlite3

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


    def __get_user(self, chat_id: int):
        self.__cursor.execute("SELECT description, lon, lat FROM users WHERE chat_id = ?", (chat_id,))
        return self.__cursor.fetchone()

    def is_correct_coord(self, chat_id: int) -> bool:
        data = self.__get_user(chat_id)
        return data[2] != 0.0 or data[1] != 0.0

    def get_user(self, chat_id: int) -> set:

        data = self.__get_user(chat_id)

        if data:
            return {
                "description": data[0],
                "lon": data[1],
                "lat": data[2]
            }
        
        return {}

    def get_title(self, data_user: set) -> str:

        if data_user["description"]:
            return data_user["description"]

        return f"Ширина: <b>{data_user['lat']}</b> Долгота: <b>{data_user['lon']}</b>\n"

    def update_city(self, chat_id: int, lon: float, lat: float, description: str = ''):
        self.__cursor.execute(f"UPDATE users SET description = ?, lon = ?, lat = ? WHERE chat_id= ?;", (description, lon, lat, chat_id))
        self.__conn.commit()


        