import sqlite3
from contextlib import contextmanager

DB_NAME = 'database.db'

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()

# データベースの初期化を行う関数
def create_table():
    with get_connection() as conn:
        with open('ddl.sql', 'r', encoding='utf-8') as f:
            ddl = f.read()
            print(ddl)
            conn.executescript(ddl)
            conn.commit()

        with open('dml.sql', 'r', encoding='utf-8') as f:
            dml = f.read()
            print(dml)
            conn.executescript(dml)
            conn.commit()

# テーブルを作成する
create_table()
