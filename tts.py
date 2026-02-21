import os
from dotenv import load_dotenv
import datetime
import requests
import json
from model import TtsApiRequest

# .envファイルの内容を読み込見込む
load_dotenv()


# ttsサーバに通信して音声ファイルを作成して保存する関数
def create_audio(chat_id: int, id: int, request: TtsApiRequest):
    mode = os.environ['MODE']
    dt_now = datetime.datetime.now()

    if mode == 'RVC':
        print("rvc-tts-webuiで音声合成を行います")

        data = {
            "model_name": request.model_name,
            "speed": request.speed,
            "tts_text": request.tts_text,
            "tts_voice": request.tts_voice,
            "f0_up_key": request.f0_up_key,
            "f0_method": request.f0_method,
            "index_rate": request.index_rate,
            "protect": request.protect
        }
        json_data = json.dumps(data)
        url = f"http://{os.environ['TTS_IPADRESS']}:{os.environ['TTS_PORT']}/tts"
        headers = {'Content-Type': 'application/json'}

    elif mode == 'VITS2':
        print("Style-Bert-VITS2で音声合成を行います")

        json_data = {}
        url = f"http://{os.environ['TTS_IPADRESS']}:{os.environ['TTS_PORT']}/voice?text={request.tts_text}&encoding=UTF-8&model_name={request.model_name}&language=JP"
        headers = {}

    with requests.post(url, headers=headers, data=json_data, stream=True) as response:
        response.raise_for_status()  # エラー時は例外を発生

        # ファイルに書き込み
        file_name = str(chat_id) + '-' + str(id) + '-' + \
            dt_now.strftime('%Y_%m_%d_%H_%M_%S') + ".wav"
        with open("static/" + file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 空のチャンクをスキップ
                    f.write(chunk)

            print("音声ファイルを保存しました: " + file_name)
            return file_name
