from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from model import ChatRequest, CreateChatRequest, Message, TtsApiRequest, TtsRequest
import db
import llm
import tts

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/languages/")
async def get_languages():
    return db.get_languages()


@app.get("/characters/")
async def get_characters():
    return db.get_characters()


@app.get("/chats/")
async def get_chats():
    return db.get_chats()


@app.get("/all-messages/")
async def get_all_messages():
    return db.get_all_messages()


@app.get("/messages/{chat_id}")
async def get_messages(chat_id: int):
    # システムメッセージを含まない
    return db.get_messages(chat_id, 1)


@app.post("/create-chat/")
async def create_chat(data: CreateChatRequest):
    return db.create_chat(data.character_id)


@app.post("/chat/")
async def post_chat(data: ChatRequest):
    # ユーザのメッセージをDBに保存
    db.add_message(data.chat_id, 'user', data.content)

    # AIモデルと対話して回答を取得
    messages = [Message(**d) for d in db.get_messages(data.chat_id, 0)]
    response = llm.chat_with_model(messages)

    # AIの回答をDBに保存
    # AIの回答を返す
    return db.add_message(data.chat_id, 'assistant', response)


@app.post("/tts/")
async def create_tts(data: TtsRequest):
    chat = db.get_chat(data.chat_id)
    message = db.get_message(data.chat_id, data.id)
    character = db.get_character(chat['character_id'])

    # 音声ファイルの受信と書き込み
    request: TtsApiRequest = TtsApiRequest(
        model_name=character['model_name'],
        speed=0,
        tts_text=message['content'],
        tts_voice=character['tts_voice'],
        f0_up_key=character['f0_up_key'],
        f0_method='rmvpe',
        index_rate=1,
        protect=0.33
    )
    file_name = tts.create_audio(data.chat_id, data.id, request)
    return db.update_audio_path(data.chat_id, data.id, file_name)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
