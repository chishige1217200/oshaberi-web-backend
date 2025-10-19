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


# 言語一覧を取得する関数
def get_languages() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, value, upd_datetime FROM language ORDER BY id")
        languages = cursor.fetchall()
        return languages


# キャラクタ一覧を取得する関数
def get_characters() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, language_id, name, prompt, model_name, icon_path, tts_voice, f0_key_up, upd_datetime FROM character ORDER BY id, language_id")
        characters = cursor.fetchall()
        return characters


# チャット一覧を取得する関数
def get_chats() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, character_id, subject, upd_datetime FROM chat ORDER BY id")
        chats = cursor.fetchall()
        return chats


# 会話履歴一覧を取得する関数
def get_all_messages(id: int = 0) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT chat_id, id, language_id, role, content, audio_path, upd_datetime FROM message WHERE id >= ? ORDER BY chat_id, id", (id,))
        messages = cursor.fetchall()
        return messages


# 会話履歴一覧を取得する関数
def get_messages(chat_id: int, id: int = 0) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT chat_id, id, language_id, role, content, audio_path, upd_datetime FROM message WHERE chat_id = ? AND id >= ? ORDER BY id", (chat_id, id))
        messages = cursor.fetchall()
        return messages


# 新しいチャットIDを採番する処理
def get_next_chat_id() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) as max_id FROM chat")
        row = cursor.fetchone()
        next_id = 1 if row['max_id'] is None else row['max_id'] + 1
        return next_id


# 新しいチャットを作成する処理
def create_chat(character_id: int) -> dict:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION;")
            chat_id = get_next_chat_id()
            cursor.execute("INSERT INTO chat (id, character_id, subject) VALUES (?, ?, ?)",
                           (chat_id, character_id, get_character_name(character_id) + "とのチャット"))

            cursor.execute(
                "SELECT id, character_id, subject, upd_datetime FROM chat WHERE id = ?", (chat_id,))
            chat = cursor.fetchone()

            # systemロールのメッセージを追加（id = 0）
            cursor.execute("INSERT INTO message (chat_id, id, language_id, role, content) VALUES (?, 0, 'ja-JP', 'system', ?)",
                           (chat['id'], get_system_prompt(character_id)))
            conn.commit()

            return chat
        except ValueError:
            conn.rollback()
            raise


# キャラクタのシステムプロンプトを取得する処理
def get_system_prompt(character_id: int) -> str:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT prompt FROM character WHERE id = ? AND language_id = 'ja-JP'", (character_id,))
        system_prompt = cursor.fetchone()
        return system_prompt['prompt']


# キャラクタの名前を取得する処理
def get_character_name(character_id: int) -> str:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM character WHERE id = ? AND language_id = 'ja-JP'", (character_id,))
        character = cursor.fetchone()
        return character['name']


# メッセージを追加する処理
def add_message(chat_id: int, role: str, content: str) -> dict:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION;")
            message_id = get_next_message_id(chat_id)
            cursor.execute("INSERT INTO message (chat_id, id, language_id, role, content) VALUES (?, ?, 'ja-JP', ?, ?)",
                           (chat_id, message_id, role, content))

            cursor.execute("SELECT chat_id, id, language_id, role, content, audio_path, upd_datetime FROM message WHERE chat_id = ? AND id = ?",
                           (chat_id, message_id))
            message = cursor.fetchone()
            conn.commit()

            return message
        except ValueError:
            conn.rollback()
            raise


# 新しいメッセージIDを採番する処理
def get_next_message_id(chat_id: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MAX(id) as max_id FROM message WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()
        next_id = 1 if row['max_id'] is None else row['max_id'] + 1
        return next_id


# テーブルを作成する
create_table()
