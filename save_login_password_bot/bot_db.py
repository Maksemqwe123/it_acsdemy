import sqlite3 as sq
from collections import Generator
from sqlite3 import IntegrityError
import logging

logging.basicConfig()


class DataBase:
    def __init__(self, file_name) -> None:
        self.connection = sq.connect(file_name)
        self.cursor = self.connection.cursor()

        self._create_table()

    def _create_table(self):
        if self.connection:
            print('Database connection')
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY NOT NULL,
            login TEXT UNIQUE,
            password TEXT
            )""")
            self.connection.commit()

    def add_account(self, login: str, password: str) -> str:
        try:
            with self.connection:
                self.cursor.execute("""INSERT INTO accounts (login, password) VALUES (?, ?)""", (login, password))
                self.connection.commit()
                return 'Добавлен новый пользователь!'
        except IntegrityError:
            return 'Данные не сохранены, проверьте уникальность логина'

    def read_info(self) -> Generator:
        with self.connection:
            all_info = self.cursor.execute("""SELECT * FROM accounts""").fetchall()
            for info in all_info:
                login = info[1]
                password = info[2]
                yield f'Логин: {login} | Пароль: {password}'

    def _check_login(self, login) -> list:
        with self.connection:
            logins = self.cursor.execute("""SELECT login FROM accounts WHERE = ?""", (login, )).fetchall()
            return logins

    def delete_account(self, login) -> str:
        with self.connection:
            if self._check_login(login):
                self.cursor.execute("""DELETE FROM accounts WHERE login = ?""", (login, ))
                self.connection.commit()
                return 'Аккаунт успешно удалён'
            else:
                return 'Аккаунт не найден'

    def delete_all_accounts(self):
        with self.connection:
            self.cursor.execute("""DELETE FROM accounts""")
        return 'Все аккаунты удалины'


if __name__ == '__main__':
    db = DataBase('user_bot')
    db.add_account('вася', '87482hedyfu64')
    print(db.read_info())
    db.delete_all_accounts()
    # db.delete_account('вася')
