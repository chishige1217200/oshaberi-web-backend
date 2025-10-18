import sqlite3
from contextlib import contextmanager

DB_NAME = 'database.db'

# dict_factoryの定義
def dict_factory(cursor, row):
   d = {}
   for idx, col in enumerate(cursor.description):
       d[col[0]] = row[idx]
   return d

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    # 辞書型で結果を取得するための設定
    conn.row_factory = dict_factory
    try:
        yield conn
    finally:
        conn.close()

# データベースの初期化を行う関数
def create_table():
    with get_connection() as conn:
        with open('ddl.sql', 'r', encoding='utf-8') as f:
            ddl = f.read()
            # print(ddl)
            conn.executescript(ddl)
            conn.commit()

        with open('dml.sql', 'r', encoding='utf-8') as f:
            dml = f.read()
            # print(dml)
            conn.executescript(dml)
            conn.commit()

def get_languages():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, value, upd_datetime FROM language order by id")
        languages = cursor.fetchall()
        return languages

def get_characters():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, language_id, name, prompt, model_name, icon_path, tts_voice, f0_key_up, upd_datetime FROM character order by id, language_id")
        characters = cursor.fetchall()
        return characters

def get_chats():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, character_id, subject, upd_datetime FROM chat order by id")
        chats = cursor.fetchall()
        return chats

def get_all_messages():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id, id, language_id, role, content, audio_path, upd_datetime FROM message order by chat_id, id")
        messages = cursor.fetchall()
        return messages

def get_messages(chat_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id, id, language_id, role, content, audio_path, upd_datetime FROM message WHERE chat_id = ? order by id", (chat_id,))
        messages = cursor.fetchall()
        return messages

def get_next_chat_id():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) as max_id FROM chat")
        row = cursor.fetchone()
        next_id = 1 if row['max_id'] is None else row['max_id'] + 1
        return next_id

def create_chat(character_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat (id, character_id) VALUES (?, ?)", (get_next_chat_id(), character_id))
        conn.commit()

        cursor.execute("SELECT id, character_id, subject, upd_datetime FROM chat WHERE id = ?", (cursor.lastrowid,))
        chat = cursor.fetchone()
        return chat

# テーブルを作成する
create_table()
