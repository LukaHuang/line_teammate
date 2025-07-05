import requests
import json
from datetime import datetime

class WebhookHandler:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def save_conversation(self, user_id: str, conversation: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            'timestamp': timestamp,
            'user_id': user_id,
            'conversation': conversation
        }
        
        try:
            response = requests.post(self.webhook_url, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending webhook: {e}")
            return False