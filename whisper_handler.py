import openai
from config import OPENAI_API_KEY
import requests
import tempfile
import os

class WhisperHandler:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
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
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
        finally:
            if os.path.exists(audio_file_path):
                os.unlink(audio_file_path)