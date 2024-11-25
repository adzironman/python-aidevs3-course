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
    
    def answer_captcha_question(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Respond to question. Respond with only a number, nothing else."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    
    def answer_question(self, question: str, model: str = "gpt-4o-mini", system_message: str = "", response_format: str = "text") -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ],
            response_format={"type": response_format}
        )
        return response.choices[0].message.content