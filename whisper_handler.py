import openai
import os
import requests
import tempfile
from config import OPENAI_API_KEY

class WhisperHandler:
    def __init__(self):
        # 詳細檢查環境變數
        env_key = os.getenv('OPENAI_API_KEY')
        config_key = OPENAI_API_KEY
        
        print(f"Environment OPENAI_API_KEY: {'SET' if env_key else 'NOT SET'}")
        print(f"Config OPENAI_API_KEY: {'SET' if config_key else 'NOT SET'}")
        
        api_key = env_key or config_key
        
        if api_key and api_key.strip():
            try:
                # 確保 API key 格式正確
                if not api_key.startswith('sk-'):
                    print(f"Warning: API key format seems incorrect: {api_key[:20]}...")
                
                # 使用最新版本，但不傳入可能導致問題的參數
                self.client = openai.OpenAI(
                    api_key=api_key.strip(),
                    timeout=60.0
                )
                print(f"✅ OpenAI client initialized successfully: {api_key[:15]}...")
            except Exception as e:
                print(f"❌ Failed to initialize OpenAI client: {e}")
                print(f"Error type: {type(e)}")
                # 如果新版本失敗，嘗試最簡單的初始化
                try:
                    self.client = openai.OpenAI(api_key=api_key.strip())
                    print("✅ OpenAI client initialized with minimal config")
                except Exception as e2:
                    print(f"❌ Minimal config also failed: {e2}")
                    self.client = None
        else:
            print("❌ OpenAI API key not found or empty")
            print(f"env_key: {env_key}")
            print(f"config_key: {config_key}")
            self.client = None
    
    def download_audio(self, audio_url: str, access_token: str) -> str:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(audio_url, headers=headers)
        
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.m4a') as temp_file:
                temp_file.write(response.content)
                return temp_file.name
        else:
            raise Exception(f"Failed to download audio: {response.status_code}")
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        if not self.client:
            print("OpenAI API key not configured, skipping audio transcription")
            return "語音轉文字功能未設定 OpenAI API 金鑰"
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                # 使用最新版本的 API
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            print(f"✅ Audio transcribed successfully: {transcript.text[:50]}...")
            return transcript.text
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            return f"語音轉換錯誤: {str(e)}"
        finally:
            if os.path.exists(audio_file_path):
                os.unlink(audio_file_path)