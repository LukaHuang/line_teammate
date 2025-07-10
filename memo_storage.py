from datetime import datetime
from typing import Dict, List
import json
import os
import threading
import time

class MemoStorage:
    def __init__(self, storage_file: str = "conversations_memory.json"):
        self.conversations: Dict[str, List[Dict]] = {}
        self.storage_file = storage_file
        self.auto_save_interval = 300  # 5分鐘自動保存
        self.last_save_time = time.time()
        self._load_from_file()
        self._start_auto_save_thread()
    
    def add_message(self, user_id: str, message: str, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            'message': message,
            'timestamp': timestamp.isoformat()
        })
        
        # 自動保存檢查
        current_time = time.time()
        if current_time - self.last_save_time > self.auto_save_interval:
            self._save_to_file()
            self.last_save_time = current_time
    
    def get_conversation(self, user_id: str) -> List[Dict]:
        return self.conversations.get(user_id, [])
    
    def clear_conversation(self, user_id: str):
        if user_id in self.conversations:
            del self.conversations[user_id]
        self._save_to_file()  # 立即保存清除操作
    
    def format_conversation(self, user_id: str, max_messages: int = None) -> str:
        messages = self.get_conversation(user_id)
        if not messages:
            return ""
        
        # 如果沒有設定 max_messages，顯示所有訊息
        if max_messages is None:
            recent_messages = messages
        else:
            # 只顯示最近的 max_messages 條訊息
            recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
        
        formatted = []
        for msg in recent_messages:
            formatted.append(msg['message'])
        
        return "\n".join(formatted)
    
    def _load_from_file(self):
        """從文件載入對話記錄"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.conversations = json.load(f)
                print(f"載入 {len(self.conversations)} 個用戶的對話記錄")
        except Exception as e:
            print(f"載入對話記錄失敗: {e}")
            self.conversations = {}
    
    def _save_to_file(self):
        """保存對話記錄到文件"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存對話記錄失敗: {e}")
    
    def _start_auto_save_thread(self):
        """啟動自動保存背景線程"""
        def auto_save():
            while True:
                time.sleep(self.auto_save_interval)
                if self.conversations:  # 只有在有對話時才保存
                    self._save_to_file()
        
        thread = threading.Thread(target=auto_save, daemon=True)
        thread.start()
    
    def get_total_messages(self) -> int:
        """獲取所有用戶的總訊息數"""
        total = 0
        for user_messages in self.conversations.values():
            total += len(user_messages)
        return total
    
    def get_user_message_count(self, user_id: str) -> int:
        """獲取指定用戶的訊息數"""
        return len(self.conversations.get(user_id, []))
    
    def force_save(self):
        """強制保存所有對話記錄"""
        self._save_to_file()
        self.last_save_time = time.time()