

import os
import io

import edge_tts

class edgeTTS:
    def __init__(self):
        self.model_ids = {
            "en": "en-US-AvaMultilingualNeural", 
            "zh": "zh-CN-XiaoyiNeural", 
            "jp": "ja-JP-NanamiNeural",
            "de": "de-DE-KatjaNeural",
            "ru": "ru-RU-DmitryNeural",
        }
        
        self.set_tts_model("")


    def set_tts_model(self, language_code):
        if language_code in self.model_ids:
            self.tts_model_id = self.model_ids[language_code]
        else:
            self.tts_model_id = self.model_ids["en"]


    async def tts(self, text):
        voice = self.tts_model_id
        communicate = edge_tts.Communicate(text, voice)
        audio_data = io.BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])

        return audio_data.getvalue()   # Read the entire audio data as bytes
    
