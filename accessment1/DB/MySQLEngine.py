import pymysql
from pymysql.cursors import DictCursor
from DB.DBEngine import DBEngine
from Log import *


class MySQLEngine(DBEngine):
    def __init__(self, host, user, password, database, port=3306):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset="utf8mb4",
            autocommit=False,         
            cursorclass=DictCursor   
        )
        self.cursor = self.conn.cursor()

    @debug_sql
    def execute(self, sql, params=()):
        self.cursor.execute(sql, params)

    @debug_sql
    def executescript(self, sql):
     
        # PyMySQL does NOT support executescript natively.
        # Split SQL manually for compatibility with SQLiteEngine.
        for stmt in sql.split(";"):
            stmt = stmt.strip()
            if stmt:
                self.cursor.execute(stmt)

    @debug_sql
    def fetch(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()