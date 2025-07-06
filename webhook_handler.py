import requests
import json
from datetime import datetime

class WebhookHandler:
    def __init__(self, webhook_url=None):
        # Webhook URL 從環境變數或參數取得
        import os
        from config import GOOGLE_SHEETS_WEBHOOK_URL
        
        env_url = os.getenv('GOOGLE_SHEETS_WEBHOOK_URL')
        config_url = GOOGLE_SHEETS_WEBHOOK_URL
        
        print(f"Environment GOOGLE_SHEETS_WEBHOOK_URL: {'SET' if env_url else 'NOT SET'}")
        print(f"Config GOOGLE_SHEETS_WEBHOOK_URL: {'SET' if config_url else 'NOT SET'}")
        
        self.webhook_url = webhook_url or env_url or config_url
        
        if self.webhook_url:
            print(f"✅ Google Sheets Webhook configured: {self.webhook_url[:50]}...")
        else:
            print("❌ Google Sheets Webhook not configured")
    
    def save_conversation(self, user_id: str, conversation: str):
        if not self.webhook_url:
            print("❌ Google Sheets Webhook URL not configured, skipping")
            return False
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            'timestamp': timestamp,
            'user_id': user_id,
            'conversation': conversation
        }
        
        print(f"🔄 Sending data to Google Sheets webhook...")
        print(f"URL: {self.webhook_url[:50]}...")
        print(f"Data: {json.dumps(data, ensure_ascii=False)[:100]}...")
        
        try:
            response = requests.post(
                self.webhook_url, 
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"📡 Webhook response: {response.status_code}")
            print(f"Response text: {response.text[:200]}")
            
            if response.status_code == 200:
                print(f"✅ Conversation saved to Google Sheets via webhook for user {user_id}")
                return True
            else:
                print(f"❌ Webhook request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending webhook: {e}")
            print(f"Exception type: {type(e)}")
            return False
    
    def save_link(self, user_id: str, link: str):
        """儲存連結到收藏連結工作表"""
        if not self.webhook_url:
            print("❌ Google Sheets Webhook URL not configured for link saving")
            return False
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            'type': 'link',  # 指定類型為連結
            'timestamp': timestamp,
            'user_id': user_id,
            'link': link
        }
        
        print(f"🔗 Sending link to Google Sheets webhook...")
        print(f"URL: {self.webhook_url[:50]}...")
        print(f"Link: {link}")
        
        try:
            response = requests.post(
                self.webhook_url, 
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"📡 Link webhook response: {response.status_code}")
            print(f"Response text: {response.text[:200]}")
            
            if response.status_code == 200:
                print(f"✅ Link saved to Google Sheets for user {user_id}")
                return True
            else:
                print(f"❌ Link webhook request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending link webhook: {e}")
            return False
    
    def save_image(self, user_id: str, image_url: str, message_id: str):
        """儲存圖片到 Google Sheets"""
        if not self.webhook_url:
            print("❌ Google Sheets Webhook URL not configured for image saving")
            return False
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            'type': 'image',  # 指定類型為圖片
            'timestamp': timestamp,
            'user_id': user_id,
            'image_url': image_url,
            'message_id': message_id
        }
        
        print(f"🖼️ Sending image to Google Sheets webhook...")
        print(f"URL: {self.webhook_url[:50]}...")
        print(f"Image URL: {image_url}")
        
        try:
            response = requests.post(
                self.webhook_url, 
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"📡 Image webhook response: {response.status_code}")
            print(f"Response text: {response.text[:200]}")
            
            if response.status_code == 200:
                print(f"✅ Image saved to Google Sheets for user {user_id}")
                return True
            else:
                print(f"❌ Image webhook request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending image webhook: {e}")
            return False