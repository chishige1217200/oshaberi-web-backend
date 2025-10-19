import os
from dotenv import load_dotenv
import requests
from model import Message, OllamaMessageRequest

# .envファイルの内容を読み込見込む
load_dotenv()


# AIモデルと対話する関数
def chat_with_model(messages: list[Message]) -> str:
    url = f"http://{os.environ['OLLAMA_IPADRESS']}:{os.environ['OLLAMA_PORT']}/api/chat"
    headers = {'Content-Type': 'application/json'}

    # OLLAMAに渡すメッセージ形式に変換
    request_messages: list[OllamaMessageRequest] = []

    for message in messages:
        request_messages.append({
            "role": message.role,
            "content": message.content
        })

    data = {
        "model": f"{os.environ['MODEL_NAME']}",
        "messages": request_messages,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()['message']['content']
