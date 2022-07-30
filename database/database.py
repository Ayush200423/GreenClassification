from db_setup import db_connect

class Database:
    def __init__(self):
        self.mysql_db = db_connect
        self.db_cursor = self.mysql_db.cursor()

    def add_user(self, username, password):
        self.db_cursor.execute("SELECT username FROM users")
        for u_name in self.db_cursor:
            if u_name[0] == username:
                raise Exception('Error: User already exists.')
        self.db_cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        self.commit()
        self.db_cursor.execute("INSERT INTO user_points (username, points) VALUES (%s, %s)", (username, 0))
        self.commit()
        return

    def authenticate_user(self, username, u_pass):
        self.db_cursor.execute(f"SELECT password FROM users WHERE username = '{username}'")
        for password in self.db_cursor:
            if password[0] == u_pass:
                self.username = username
                return True
            return False

    def get_points(self):
        self.db_cursor.execute(f"SELECT points FROM user_points WHERE username = '{self.username}'")
        for points in self.db_cursor:
            return points[0]

    def add_point(self, current_points):
        current_points += 1
        self.db_cursor.execute(f"UPDATE user_points SET points = {current_points} WHERE username = '{self.username}'")
        self.commit()

    def commit(self):
        self.mysql_db.commit()

db = Database()
print(db.get_points("Ayush"))