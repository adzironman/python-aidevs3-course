import os
import logging
from typing import List
from openai import OpenAI
from pydub import AudioSegment

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    def transcribe_audio(self, chunk_paths: List[str]) -> str:
        """Transcribe multiple audio chunks and combine them."""
        transcriptions = []
        
        for chunk_path in chunk_paths:
            with open(chunk_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                logging.info(f"Transcription for {chunk_path}: {transcript}")
                transcriptions.append(transcript)
        
        return " ".join(transcriptions)