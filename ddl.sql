CREATE TABLE IF NOT EXISTS character (
    id INTEGER,
    prompt TEXT NOT NULL,
    model_name TEXT NOT NULL,
    ja_tts_voice TEXT NOT NULL default 'ja-JP-NanamiNeural-Female',
    en_tts_voice TEXT NOT NULL default 'en-US-AriaNeural-Female',
    f0_key_up INTEGER NOT NULL default 0,
    upd_datetime TEXT NOT NULL default CURRENT_TIMESTAMP, -- 'YYYY-MM-DD HH:MM:SS'形式で保存
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS talk (
    id INTEGER,
    character_id INTEGER NOT NULL,
    subject TEXT,
    upd_datetime TEXT NOT NULL default CURRENT_TIMESTAMP, -- 'YYYY-MM-DD HH:MM:SS'形式で保存
    PRIMARY KEY (id),
    FOREIGN KEY (character_id) REFERENCES character(id)
);

CREATE TABLE IF NOT EXISTS chat (
    talk_id INTEGER NOT NULL,
    id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    audio_path TEXT,
    upd_datetime TEXT NOT NULL default CURRENT_TIMESTAMP,
    PRIMARY KEY (talk_id, id),
    FOREIGN KEY (talk_id) REFERENCES talk(id)
);
