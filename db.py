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
    with open('ddl.sql', 'r', encoding='utf-8') as f:
        ddl = f.read()
        print(ddl)
        with get_connection() as conn:
            conn.executescript(ddl)
            conn.commit()

# テーブルを作成する
create_table()
