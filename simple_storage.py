from datetime import datetime
import json
import os

class SimpleStorage:
    def __init__(self, storage_file='conversations.json'):
        self.storage_file = storage_file
        self.conversations = self.load_conversations()
    
    def load_conversations(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_conversations(self):
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def save_conversation(self, user_id: str, conversation: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = {
            'timestamp': timestamp,
            'user_id': user_id,
            'conversation': conversation
        }
        
        # 儲存到檔案
        self.conversations.append(log_entry)
        success = self.save_conversations()
        
        # 同時印出日誌
        print(f"[CONVERSATION LOG] {json.dumps(log_entry, ensure_ascii=False)}")
        
        return success