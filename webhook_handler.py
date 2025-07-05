import requests
import json
from datetime import datetime

class WebhookHandler:
    def __init__(self, webhook_url=None):
        # Webhook URL 從環境變數或參數取得
        from config import GOOGLE_SHEETS_WEBHOOK_URL
        self.webhook_url = webhook_url or GOOGLE_SHEETS_WEBHOOK_URL
    
    def save_conversation(self, user_id: str, conversation: str):
        if not self.webhook_url:
            print("Google Sheets Webhook URL not configured")
            return False
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            'timestamp': timestamp,
            'user_id': user_id,
            'conversation': conversation
        }
        
        try:
            response = requests.post(
                self.webhook_url, 
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Conversation saved to Google Sheets via webhook for user {user_id}")
                return True
            else:
                print(f"Webhook request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error sending webhook: {e}")
            return False