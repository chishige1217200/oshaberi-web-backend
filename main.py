from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import db

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
    return db.get_messages(chat_id)

@app.post("/create-chat/")
async def create_chat(data: dict):
    # チャットを作成するための処理を実装
    return {"received": data}

@app.post("/chat/")
async def post_chat(data: dict):

    return {"received": data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
