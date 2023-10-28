import sqlite3

class Database():
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    def create_tables(self):
        with self.connection:
            users = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    user_id TEXT,
                    info TEXT,
                    nickname TEXT);
                """
            )
            hometask = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS hometask(
                    date TEXT,
                    subject TEXT,
                    task TEXT,
                    document TEXT);
                """
            )
    def add_user(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`user_id`, `info`, `nickname`) VALUES (?,?,?)", (user_id, 'Пусто', nickname)
            )

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return bool(result)
    def get_user(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchone()
            return res
    def get_all_users(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM users"
            ).fetchall()
    def set_info(self, user_id, info):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET info = ? WHERE user_id = ?", (info, user_id,)
            )
    def get_id_from_nick(self, nick):
        with self.connection:
            return self.cursor.execute(
                "SELECT user_id FROM users WHERE nickname = ?", (nick,)
            ).fetchone()
    def add_task(self, date, subject, task, doc_path):
        with self.connection:
            docs = ''
            for doc in doc_path:
                docs += '|' + doc
            return self.cursor.execute(
                "INSERT INTO hometask (date, subject, task, document) VALUES (?,?,?,?)", (date, subject, task, docs)
            )
    def get_date_tasks(self, date):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM hometask WHERE date = ?", (date,)
            ).fetchall()
    def del_task(self, date, subject):
        with self.connection:
            if subject == 'all':
                return self.cursor.execute(
                    "DELETE FROM hometask WHERE date = ?", (date,)
                )
            return self.cursor.execute(
                    "DELETE FROM hometask WHERE date = ? AND subject = ?", (date,subject,)
            )
    def get_all_dates(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT date FROM hometask'
            ).fetchall()
    def get_subject_files(self, date, subject):
        with self.connection:
            return self.cursor.execute(
                "SELECT document FROM hometask WHERE date = ? AND subject = ?", (date, subject)
            ).fetchone()