import sqlite3 as sq


class DataBase:
    def __init__(self, db_file: str):
        self.connection = sq.connect(db_file)
        self.cursor = self.connection.cursor()

        self._create_table()

    def _create_table(self):
        if self.connection:
            print('good connection')
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY NOT NULL,
            user_id INTEGER UNIQUE NOT NULL,
            username VARCHAR(30),
            time_sub NOT NULL DEFAULT 0,
            signup VARCHAR(30) DEFAULT 'setusername' 
            );""")

    def add_user(self, user_id: int):
        with self.connection:
            self.cursor.execute("""INSERT INTO users (user_id) VALUES (?)""", (user_id, ))

    def read_db(self):
        with self.connection:
            result = self.cursor.execute("""SELECT * FROM users""")
            print(result.fetchall())

    def user_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id, ))
            return bool(result.fetchall())

    def set_username(self, user_id, username):
        with self.connection:
            result = self.cursor.execute("""UPDATE users SET username = ? WHERE user_id = ?""", (username, user_id))
            return result

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("""SELECT signup FROM users WHERE user_id = ? """, (user_id, )).fetchall()
            return result[0][0]

    def delete_user(self, user_id):
        with self.connection:
            self.cursor.execute("""DELETE FROM users WHERE user_id = ?""", (user_id, ))

    def set_signup(self, user_id, signup):
        with self.connection:
            self.cursor.execute("""UPDATE users SET signup = ? WHERE user_id = ?""", (signup, user_id))

    def get_username(self, user_id):
        with self.connection:
            result = self.cursor.execute("""SELECT username FROM users WHERE user_id = ? """, (user_id, )).fetchall()
            return result[0][0]


if __name__ == '__main__':
    db = DataBase('test.db')
    # db.add_user(362764)
    db.read_db()
    db.set_username(user_id=362764, username='Maxim')
    print(db.get_signup(362764))
    db.set_signup(362764, 'done')
