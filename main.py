from fastapi import FastAPI
import uvicorn
import db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/languages/")
async def get_languages():
    return db.get_languages()

@app.get("/chats/")
async def get_chats():
    return db.get_chats()

@app.get("/all-messages/")
async def get_all_messages():
    return db.get_all_messages()

@app.get("/messages/{chat_id}")
async def get_messages(chat_id: int):
    return db.get_messages(chat_id)

@app.post("/chat/")
async def post_chat(data: dict):

    return {"received": data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
