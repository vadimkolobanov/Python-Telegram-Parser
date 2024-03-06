import logging
import sqlite3
from sqlite3 import IntegrityError


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        # Подключение к базе данных
        self.connection = sqlite3.connect(self.db_name)

    def create_tables(self):
        # Создание таблиц
        cursor = self.connection.cursor()

        # Создание таблицы "Users"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                access_hash TEXT,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                phone TEXT,
                photo_id INTEGER,
                status TEXT,
                channel_id INTEGER,
                FOREIGN KEY (photo_id) REFERENCES ProfilePhotos(id),
                FOREIGN KEY (channel_id) REFERENCES Channels(id),
                UNIQUE (channel_id, id)
            )
        ''')

        # Создание таблицы "ProfilePhotos"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProfilePhotos (
                id INTEGER PRIMARY KEY,
                file_path TEXT,
                other_details TEXT
            )
        ''')

        # Создание таблицы "Channels"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Channels (
                id INTEGER PRIMARY KEY,
                name TEXT,
                link TEXT,
                date_created DATETIME
            )
        ''')

        # Создание таблицы "Messages"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                channel_id INTEGER,
                date DATETIME,
                message TEXT,
                out INTEGER,
                mentioned INTEGER,
                media_unread INTEGER,
                silent INTEGER,
                post INTEGER,
                reply_to INTEGER,
                views INTEGER,
                forwards INTEGER,
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (channel_id) REFERENCES Channels(id),
                FOREIGN KEY (reply_to) REFERENCES Messages(id),
                UNIQUE (channel_id, id)
            )
        ''')

        self.connection.commit()

    def execute_query(self, query, *args):
        # Исполнение SQL-запроса
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        self.connection.commit()

    def insert_user(self, user_id, access_hash, first_name, last_name, username, phone, photo_id, status, channel_id):
        query = '''
            INSERT OR IGNORE INTO Users (id, access_hash, first_name, last_name, username, phone, photo_id, status, channel_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor = self.connection.cursor()
        cursor.execute(query,
                       (user_id, access_hash, first_name, last_name, username, phone, photo_id, status, channel_id))
        self.connection.commit()

    def insert_channel(self, channel_id, name, link, date_created):
        query = '''
            INSERT OR IGNORE INTO Channels (id, name, link, date_created)
            VALUES (?, ?, ?, ?)
        '''
        cursor = self.connection.cursor()
        cursor.execute(query, (channel_id, name, link, date_created))
        self.connection.commit()

    def insert_message(self, message_id, user_id, channel_id, date, message, out, mentioned, media_unread, silent, post,
                       reply_to, views, forwards):
        query = '''
            INSERT INTO Messages (id, user_id, channel_id, date, message, out, mentioned, media_unread, silent, post, reply_to, views, forwards)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        date_str = date.strftime('%Y-%m-%d %H:%M:%S')

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (
                message_id, user_id, channel_id, date_str, message, out, mentioned, media_unread, silent, post, reply_to,
                views,
                forwards))
        except IntegrityError:
            logging.warning('Обнаружено дублирование значений')
        self.connection.commit()

    def close(self):
        # Закрытие соединения с базой данных
        self.connection.close()
