import os
from dotenv import load_dotenv

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Google Sheets - 支援兩種方式
GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON')
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
GOOGLE_SHEETS_WEBHOOK_URL = os.getenv('GOOGLE_SHEETS_WEBHOOK_URL')

if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET]):
    print("ERROR: Missing required environment variables:")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("  - LINE_CHANNEL_ACCESS_TOKEN")
    if not LINE_CHANNEL_SECRET:
        print("  - LINE_CHANNEL_SECRET")
    raise ValueError("Missing required environment variables: LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET")