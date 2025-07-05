from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, AudioMessage, TextSendMessage
from memo_storage import MemoStorage
from whisper_handler import WhisperHandler
from simple_storage import SimpleStorage
from webhook_handler import WebhookHandler
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

memo_storage = MemoStorage()
whisper_handler = WhisperHandler()
storage_handler = SimpleStorage()
webhook_handler = WebhookHandler()

@app.route("/health", methods=['GET'])
def health():
    return {"status": "ok", "message": "LINE Bot is running"}, 200

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    message_text = event.message.text
    
    if message_text == '/save':
        conversation = memo_storage.format_conversation(user_id)
        if conversation:
            # 嘗試儲存到 Google Sheets (Webhook)，失敗則儲存到本地
            webhook_success = webhook_handler.save_conversation(user_id, conversation)
            local_success = storage_handler.save_conversation(user_id, conversation)
            
            if webhook_success or local_success:
                memo_storage.clear_conversation(user_id)
                if webhook_success:
                    reply_text = "對話已成功儲存到 Google Sheets！"
                else:
                    reply_text = "對話已儲存到本地檔案！"
            else:
                reply_text = "儲存失敗，請稍後再試。"
        else:
            reply_text = "沒有對話可以儲存。"
    else:
        memo_storage.add_message(user_id, message_text)
        
        # 取得累積的對話內容
        conversation_history = memo_storage.format_conversation(user_id)
        
        if conversation_history:
            reply_text = f"{conversation_history}"
        else:
            reply_text = f"{message_text}"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    user_id = event.source.user_id
    message_id = event.message.id
    
    try:
        message_content = line_bot_api.get_message_content(message_id)
        audio_url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
        
        audio_file_path = whisper_handler.download_audio(audio_url, LINE_CHANNEL_ACCESS_TOKEN)
        transcribed_text = whisper_handler.transcribe_audio(audio_file_path)
        
        if transcribed_text:
            memo_storage.add_message(user_id, transcribed_text)
            
            # 取得累積的對話內容
            conversation_history = memo_storage.format_conversation(user_id)
            
            if conversation_history:
                reply_text = f"{conversation_history}"
            else:
                reply_text = f"{transcribed_text}"
        else:
            reply_text = "語音轉換失敗，請重新發送。"
            
    except Exception as e:
        print(f"Error processing audio: {e}")
        reply_text = "處理語音時發生錯誤，請重新發送。"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    import os
    try:
        port = int(os.environ.get('PORT', 5000))
        print(f"Starting LINE Bot on port {port}")
        app.run(debug=False, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        exit(1)