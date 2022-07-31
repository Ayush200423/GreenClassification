from db_setup import db_connect

class Database:
    def __init__(self):
        self.mysql_db = db_connect
        self.db_cursor = self.mysql_db.cursor()

    def add_user(self, username, password):
        self.db_cursor.execute("SELECT * FROM users")
        for u_name in self.db_cursor:
            if u_name[0] == username:
                return Exception('Error: Double Users')
        self.db_cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        self.commit()
        self.db_cursor.execute("INSERT INTO user_points (username, points) VALUES (%s, %s)", (username, 0))
        self.commit()
        return

    def authenticate_user(self, username, u_pass):
        self.db_cursor.execute(f"SELECT password FROM users WHERE username = '{username}'")
        for password in self.db_cursor:
            if password[0] == u_pass:
                return True
            return False

    def get_points(self, username):
        self.db_cursor.execute(f"SELECT points FROM user_points WHERE username = '{username}'")
        for points in self.db_cursor:
            return points[0]

    def add_point(self, current_points, username):
        current_points += 1
        self.db_cursor.execute(f"UPDATE user_points SET points = {current_points} WHERE username = '{username}'")
        self.commit()

    def commit(self):
        self.mysql_db.commit()