import sqlite3
from DB.DBEngine import DBEngine
from Log import *
class SQLiteEngine(DBEngine):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    @debug_sql
    def execute(self, sql, params=()):
        self.cursor.execute(sql, params)
    
    @debug_sql
    def executescript(self, sql):
        self.cursor.executescript(sql)

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