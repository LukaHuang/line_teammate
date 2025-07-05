import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_SPREADSHEET_ID

class GoogleSheetsHandler:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            GOOGLE_SHEETS_CREDENTIALS_JSON, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_key(GOOGLE_SPREADSHEET_ID).sheet1
    
    def save_conversation(self, user_id: str, conversation: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            self.sheet.append_row([timestamp, user_id, conversation])
            return True
        except Exception as e:
            print(f"Error saving to Google Sheets: {e}")
            return False