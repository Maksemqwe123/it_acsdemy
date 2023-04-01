import sqlite3
import logging
import uuid
from datetime import datetime, timedelta
from pprint import pprint
from typing import Union

from RimenderBot.config.config_reader import load_config

config = load_config(r'Z:\Troshkin Artem\Pt9\Maxim Markovtsov\RimenderBot\config\config.ini')


class Mysqlite:
    def __init__(self, file_db):
        self.conn = sqlite3.connect(file_db)
        self.cursor = self.conn.cursor()

        self._create_table_users()

    def _create_table_users(self):
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS remember_users (
            id INT,
            user_id INT,
            name TEXT,
            date TEXT,
            text TEXT
            );""")

    def insert_table_users(self, user_id: int, name: str, date: str, text: str, _id=None) -> Union[bool, int, tuple]:
        """
        Вставка напоминаний в БД
        :param user_id: id пользователя в тг
        :param name: имя пользователя в тг
        :param date: дата, в которую должно прийти напоминание
        :param text: текст напоминаний
        :param _id: уникальный id записи в БД
        :return: bool, status code
        """

        try:
            if not _id:
                value = (str(uuid.uuid4()), user_id, name, date, text)

            else:
                value = (user_id, name, date, text)
            if not self._check_duplicates(value):
                with self.conn:
                    self.cursor.execute(
                        f"""INSERT INTO remember_users (id, user_id, name, date, text) VALUES (?, ?, ?, ?, ?)""", value
                    )
                    return True, 200, value

            else:
                return False, 404, value

        except Exception as ex:
            logging.error(repr(ex))
            return False, 404, repr(ex)

    def _check_duplicates(self, value: tuple) -> bool:
        """
        Проверка на дубликаты
        :param value: картеж значений
        :return:
        """

        with self.conn:
            all_data = self.cursor.execute("""SELECT user_id, name, date, text FROM remember_users""")
            for remind in all_data.fetchall():
                if remind == value[1:]:
                    return True

    def get_all_value_json(self):
        """Получение всех значений из БД

        :return:
        """

        try:
            with self.conn:
                all_data = self.cursor.execute("""SELECT * FROM remember_users""")
                all_posts = self._get_formatted_json(all_data.fetchall())
                return all_posts, 200

        except Exception as ex:
            logging.error(repr(ex))
            return repr(ex), 404

    def _get_formatted_json(self, users: Union[list, tuple]):
        """Возвращает данные в формате JSON"""
        all_posts = dict()
        for user in users:
            _id = user[0]
            user_id = user[1]
            name = user[2]
            date = user[3]
            text = user[4]
            all_posts[_id] = {
                'user_id': user_id,
                'name': name,
                'date': date,
                'text': text
            }

        return all_posts

    def delete_all_user(self):
        with self.conn:
            try:
                self.cursor.execute("""DELETE FROM remember_users""")
                return 'Все значение удаленны'
            except Exception as ex:
                logging.error(repr(ex))
                return repr(ex), 404

    def send_remind(self):
        """
        Отправка напломинаний
        :return: user_id, name, text
        """

        with self.conn:
            time_direction = config.tg_bot.TIME_DIRECTION
            now = datetime.now() + timedelta(hours=time_direction)
            now_date = now.strftime('%H:%M - %d.%m.%Y')
            result = self.cursor.execute("SELECT * FROM remember_users WHERE date = ?", (now_date, ))

            all_data = result.fetchall()
            if all_data:
                all_id = tuple(
                    [_id[0] for _id in all_data]
                )
                self._delete_values(all_id)
                for value in all_data:
                    user_id = value[1]
                    name = value[2]
                    text = value[3]
                    yield user_id, name, text
            else:
                return None

    def _delete_values(self, all_id: tuple):
        """
        Удаление значений по id
        """
        with self.conn:
            for _id in all_id:
                self.cursor.execute("""DELETE FROM remember_users WHERE id = ?""", (_id, ))


if __name__ == '__main__':
    db = Mysqlite(r'Z:\Troshkin Artem\Pt9\Maxim Markovtsov\RimenderBot\database\database.db')
    print(db.insert_table_users(user_id=123456789, name='Maxim', date='23-12-13 00:20:00', text='Важное напоминание'))
    pprint(db.get_all_value_json()[0])

