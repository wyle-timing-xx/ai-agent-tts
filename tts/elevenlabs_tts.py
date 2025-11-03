from elevenlabs import ElevenLabs, VoiceSettings
from tts.tts import TTS
from videosdk.stream import MediaStreamTrack


class ElevenLabsTTS(TTS):
    def __init__(self, api_key: str, output_track: MediaStreamTrack):
      self.elevenlabs_client = ElevenLabs(api_key=api_key)
      self.model = "eleven_multilingual_v2"
      self.output_track = output_track

    def generate(self, text):
        """Start the text-to-speech listening process."""
        tts_bytes = self.elevenlabs_client.generate(
            text=text,
            stream=True,
            output_format="pcm_24000",
            model=self.model,

            voice_settings=VoiceSettings(
                stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True
            )
        )
        self.output_track.add_new_bytes(
            bytes=tts_bytes
        )