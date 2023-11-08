import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            users = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    user_id TEXT,
                    info TEXT,
                    nickname TEXT,
                    ban TEXT);
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
            soc_rate = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS soc_rate(
                    lastname TEXT,
                    rating TEXT,
                    history TEXT);
                """
            )

    def add_user(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`user_id`, `info`, `nickname`) VALUES (?,?,?)",
                (user_id, "Пусто", nickname),
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
            return self.cursor.execute("SELECT * FROM users").fetchall()

    def set_info(self, user_id, info):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET info = ? WHERE user_id = ?",
                (
                    info,
                    user_id,
                ),
            )

    def get_id_from_nick(self, nick):
        with self.connection:
            return self.cursor.execute(
                "SELECT user_id FROM users WHERE nickname = ?", (nick,)
            ).fetchone()

    def get_id_from_lastname(self, lastname):
        with self.connection:
            for user in self.get_all_users():
                if user[1].split()[1] == lastname:
                    return user[0]

    def add_task(self, date, subject, task, doc_path):
        with self.connection:
            docs = ""
            for doc in doc_path:
                docs += "|" + doc
            return self.cursor.execute(
                "INSERT INTO hometask (date, subject, task, document) VALUES (?,?,?,?)",
                (date, subject, task, docs),
            )

    def get_date_tasks(self, date):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM hometask WHERE date = ?", (date,)
            ).fetchall()

    def del_task(self, date, subject):
        with self.connection:
            if subject == "all":
                return self.cursor.execute(
                    "DELETE FROM hometask WHERE date = ?", (date,)
                )
            return self.cursor.execute(
                "DELETE FROM hometask WHERE date = ? AND subject = ?",
                (
                    date,
                    subject,
                ),
            )

    def get_all_dates(self):
        with self.connection:
            return self.cursor.execute("SELECT date FROM hometask").fetchall()

    def get_subject_files(self, date, subject):
        with self.connection:
            return self.cursor.execute(
                "SELECT document FROM hometask WHERE date = ? AND subject = ?",
                (date, subject),
            ).fetchone()

    def get_rate(self, lastname):
        with self.connection:
            return self.cursor.execute(
                "SELECT rating FROM soc_rate WHERE lastname = ?", (lastname,)
            ).fetchone()

    def get_all_rates(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM soc_rate").fetchall()

    def add_rate(self, lastname):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO soc_rate (lastname, rating, history) VALUES (?,?,?)",
                (lastname, 0, ""),
            )

    def get_history(self, lastname):
        with self.connection:
            return self.cursor.execute(
                "SELECT history FROM soc_rate WHERE lastname = ?", (lastname,)
            ).fetchone()

    def add_history(self, lastname, new_note):
        with self.connection:
            prev_history = self.get_history(lastname)[0]
            new_history = prev_history + new_note + "/"
            return self.cursor.execute(
                "UPDATE soc_rate SET history = ? WHERE lastname = ?",
                (
                    new_history,
                    lastname,
                ),
            )

    def change_rate(self, lastname, rate, new_note):
        with self.connection:
            self.add_history(lastname, new_note)
            prev_rate = self.get_rate(lastname)[0]
            if self.get_rate(lastname)[0] == "0":
                new_rate = int(rate)
            else:
                new_rate = int(prev_rate) + int(rate)
            return self.cursor.execute(
                "UPDATE soc_rate SET rating = ? WHERE lastname = ?",
                (new_rate, lastname),
            )

    def ban(self, userid):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET ban = 1 WHERE user_id = ?", (userid,)
            )

    def unban(self, userid):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET ban = 0 WHERE user_id = ?", (userid,)
            )
