import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
from config import GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_SPREADSHEET_ID

class GoogleSheetsHandler:
    def __init__(self):
        if not GOOGLE_SHEETS_CREDENTIALS_JSON or not GOOGLE_SPREADSHEET_ID:
            print("Google Sheets credentials not configured")
            self.client = None
            self.sheet = None
            return
            
        try:
            self.scope = ['https://spreadsheets.google.com/feeds',
                         'https://www.googleapis.com/auth/drive']
            
            # 支援 JSON 字串格式的憑證
            if GOOGLE_SHEETS_CREDENTIALS_JSON.startswith('{'):
                # 如果是 JSON 字串
                credentials_dict = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)
                self.creds = ServiceAccountCredentials.from_json_keyfile_dict(
                    credentials_dict, self.scope)
            else:
                # 如果是檔案路徑
                self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                    GOOGLE_SHEETS_CREDENTIALS_JSON, self.scope)
            
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open_by_key(GOOGLE_SPREADSHEET_ID).sheet1
            print("Google Sheets initialized successfully")
            
        except Exception as e:
            print(f"Failed to initialize Google Sheets: {e}")
            self.client = None
            self.sheet = None
    
    def save_conversation(self, user_id: str, conversation: str):
        if not self.sheet:
            print("Google Sheets not configured, skipping save")
            return False
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            self.sheet.append_row([timestamp, user_id, conversation])
            print(f"Conversation saved to Google Sheets for user {user_id}")
            return True
        except Exception as e:
            print(f"Error saving to Google Sheets: {e}")
            return False