from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

class Database:

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
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