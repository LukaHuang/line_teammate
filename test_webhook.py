#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def test_webhook():
    webhook_url = "https://script.google.com/macros/s/AKfycbxJva6-nNIv7sephEhOZDDjhsUpqGrV-JpfOSCzGeAzFYCyf6FVE_mX3tMkAribXqTM/exec"
    
    # 測試資料
    test_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': 'test_user_123',
        'conversation': '測試對話內容\n第二行測試'
    }
    
    print("🔄 Testing Google Sheets Webhook...")
    print(f"URL: {webhook_url}")
    print(f"Data: {json.dumps(test_data, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_webhook()