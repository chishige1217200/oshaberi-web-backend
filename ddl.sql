CREATE TABLE
    IF NOT EXISTS language (
        id TEXT NOT NULL DEFAULT 'ja-JP',
        value TEXT NOT NULL DEFAULT '日本語',
        upd_datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 'YYYY-MM-DD HH:MM:SS'形式で保存
        PRIMARY KEY (id)
    );

CREATE TABLE
    IF NOT EXISTS character(
        id INTEGER NOT NULL,
        language_id TEXT NOT NULL DEFAULT 'ja-JP',
        name TEXT NOT NULL DEFAULT '名無し',
        prompt TEXT NOT NULL,
        model_name TEXT NOT NULL,
        icon_path TEXT NOT NULL DEFAULT 'sample.png',
        tts_voice TEXT NOT NULL DEFAULT 'ja-JP-NanamiNeural-Female',
        f0_key_up INTEGER NOT NULL DEFAULT 0,
        upd_datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 'YYYY-MM-DD HH:MM:SS'形式で保存
        PRIMARY KEY (id, language_id),
        FOREIGN KEY (language_id) REFERENCES language (id)
    );

CREATE TABLE
    IF NOT EXISTS chat (
        id INTEGER NOT NULL,
        character_id INTEGER NOT NULL,
        subject TEXT NOT NULL DEFAULT '新しいチャット',
        upd_datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 'YYYY-MM-DD HH:MM:SS'形式で保存
        PRIMARY KEY (id),
        FOREIGN KEY (character_id) REFERENCES character(id)
    );

CREATE TABLE
    IF NOT EXISTS message (
        chat_id INTEGER NOT NULL,
        id INTEGER NOT NULL,
        language_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        audio_path TEXT,
        upd_datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (chat_id, id),
        FOREIGN KEY (chat_id) REFERENCES chat (id),
        FOREIGN KEY (language_id) REFERENCES character(language_id)
    );