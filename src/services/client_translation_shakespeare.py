import json
from typing import Optional

from google.cloud import texttospeech
from google.oauth2 import service_account

from src.bootstrap_stages.stage01 import config
from src.bootstrap_stages.stage04.tts_config import config as tts_config
from src.core import SingletonMeta
from src.enums.languages import LanguageEnum
from src.enums.tts_voice_name import GoogleWaveNetCustomVoiceName


class ClientTranslationShakespeare(metaclass=SingletonMeta):

    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3
    profile_id: str = "telephony-class-application"

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_info(json.loads(config.GCP_CREDENTIALS))
        self.tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

    def synthesize(self, text: str = None, ssml: str = None, voice_name=GoogleWaveNetCustomVoiceName.normal_woman,
                   language=LanguageEnum.arabic.value)\
            -> Optional[texttospeech.SynthesizeSpeechResponse]:
        if not text and not ssml:
            return

        voice_config = tts_config.language2voice_config[language][voice_name]

        synthesis_input = texttospeech.SynthesisInput(text=text, ssml=ssml)

        voice = texttospeech.VoiceSelectionParams(
            language_code=voice_config.language,
            name=voice_config.google_voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=self.audio_encoding,
            pitch=voice_config.pitch,
            speaking_rate=voice_config.speaking_rate,
            sample_rate_hertz=config.TTS_AUDIO_SAMPLE_RATE,
            effects_profile_id=[config.TTS_AUDIO_DEVICE_PROFILE]
        )

        return self.tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
