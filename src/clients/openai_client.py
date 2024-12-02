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
    
    def generate_image(self, prompt: str, model: str = "dall-e-3", size: str = "1024x1024", quality: str = "standard") -> str:
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality
        )
        return response.data[0].url
    
    def read_text_from_image(self, image_path: str) -> str:
        # Convert image to base64
        with open(image_path, "rb") as image_file:
            import base64
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a text extraction assistant. Please read and return all text visible in the image."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please read and extract all text from this image."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content