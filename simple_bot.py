from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, AudioMessage, TextSendMessage
import openai
import tempfile
import os

app = Flask(__name__)

# 設定 API 金鑰
LINE_TOKEN = "YOUR_LINE_TOKEN"
LINE_SECRET = "YOUR_LINE_SECRET" 
OPENAI_KEY = "YOUR_OPENAI_KEY"

line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
openai.api_key = OPENAI_KEY

# 儲存對話
conversations = {}

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    handler.handle(body, signature)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    user_id = event.source.user_id
    text = event.message.text
    
    if text == '/save':
        # 儲存對話到檔案
        if user_id in conversations:
            with open(f'memo_{user_id}.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(conversations[user_id]))
            conversations[user_id] = []
            reply = "對話已儲存！"
        else:
            reply = "沒有對話可儲存"
    else:
        # 記錄文字訊息
        if user_id not in conversations:
            conversations[user_id] = []
        conversations[user_id].append(text)
        reply = "已記錄！"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    user_id = event.source.user_id
    
    # 下載語音檔案
    message_content = line_bot_api.get_message_content(event.message.id)
    
    with tempfile.NamedTemporaryFile(suffix='.m4a', delete=False) as temp_file:
        for chunk in message_content.iter_content():
            temp_file.write(chunk)
        temp_path = temp_file.name
    
    # 轉換語音為文字
    try:
        with open(temp_path, 'rb') as audio_file:
            client = openai.OpenAI(api_key=OPENAI_KEY)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        text = transcript.text
        
        # 記錄轉換後的文字
        if user_id not in conversations:
            conversations[user_id] = []
        conversations[user_id].append(text)
        
        reply = f"語音轉文字：{text}"
        
    except Exception as e:
        reply = "語音轉換失敗"
    
    finally:
        os.unlink(temp_path)
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(port=5000)