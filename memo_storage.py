from datetime import datetime
from typing import Dict, List

class MemoStorage:
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}
    
    def add_message(self, user_id: str, message: str, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            'message': message,
            'timestamp': timestamp.isoformat()
        })
    
    def get_conversation(self, user_id: str) -> List[Dict]:
        return self.conversations.get(user_id, [])
    
    def clear_conversation(self, user_id: str):
        if user_id in self.conversations:
            del self.conversations[user_id]
    
    def format_conversation(self, user_id: str, max_messages: int = 10) -> str:
        messages = self.get_conversation(user_id)
        if not messages:
            return ""
        
        # 只顯示最近的 max_messages 條訊息
        recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
        
        formatted = []
        for msg in recent_messages:
            formatted.append(msg['message'])
        
        return "\n".join(formatted)