import pymysql

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"          # À modifier selon vos configurations Workbench
        self.password = "sh$ql8-R3rationer@030925!"  # À modifier
        self.database = "gestion_automobile"
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            return self.connection
        except pymysql.MySQLError as e:
            print(self.connection)
            print(f"Erreur de connexion à la base de données : {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()