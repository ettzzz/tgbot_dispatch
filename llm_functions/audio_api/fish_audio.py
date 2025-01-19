

import os
import io

from fish_audio_sdk import Session, ASRRequest, TTSRequest

class fishAudio:
    def __init__(self):
        api_key = os.getenv("FISH_AUDIO_APIKEY")
        self.session = Session(apikey=api_key)
        
        self.model_ids = {
            "en": "d764dbff171f45ba9f85ef7adca85568", ## model_id_en_conv
            "zh": "aebaa2305aa2452fbdc8f41eec852a79", ## 雷军
            "jp": "5f926f598e3458faf5f385c29f13d25", ## 七海みなみv2
            "de": "88b18e0d81474a0ca08e2ea6f9df5ff4", ## Christa deutsch
            "ru": "21ffca77b4fd41488a1fcf3fe6bbb13b", ## Putin
        }
        
        self.set_tts_model("")
        

    def set_tts_model(self, language_code):
        if language_code in self.model_ids:
            self.tts_model_id = self.model_ids[language_code]
        else:
            self.tts_model_id = self.model_ids["en"]


    def asr(self, audio_data, language_code="en"):
        request = ASRRequest(audio=audio_data, language=language_code)
        response = self.session.asr(request)
        return response.text
    
    
    def tts(self, text):
        audio_data = io.BytesIO()
        for chunk in self.session.tts(TTSRequest(
            reference_id=self.tts_model_id,
            text=text.strip()
        )):
            audio_data.write(chunk)

        return audio_data.getvalue()   # Read the entire audio data as bytes
    
