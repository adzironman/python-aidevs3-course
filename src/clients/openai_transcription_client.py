import os
from typing import List
from openai import OpenAI
import wave

class OpenAITranscriptionClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chunk_audio(self, file_path: str, chunk_duration: int = 60) -> List[str]:
        """Chunk audio file into smaller parts."""
        audio_chunks = []
        with wave.open(file_path, 'rb') as audio_file:
            frame_rate = audio_file.getframerate()
            total_frames = audio_file.getnframes()
            chunk_size = frame_rate * chunk_duration
            
            for start in range(0, total_frames, chunk_size):
                audio_file.setpos(start)
                frames = audio_file.readframes(min(chunk_size, total_frames - start))
                chunk_file_path = f"chunk_{start // chunk_size}.wav"
                with wave.open(chunk_file_path, 'wb') as chunk_file:
                    chunk_file.setnchannels(audio_file.getnchannels())
                    chunk_file.setsampwidth(audio_file.getsampwidth())
                    chunk_file.setframerate(frame_rate)
                    chunk_file.writeframes(frames)
                audio_chunks.append(chunk_file_path)
        
        return audio_chunks

    def transcribe_chunks(self, chunk_paths: List[str]) -> str:
        """Transcribe multiple audio chunks and combine them."""
        transcriptions = []
        
        for chunk_path in chunk_paths:
            with open(chunk_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                transcriptions.append(transcript)
        
        return " ".join(transcriptions)

    def transcribe_short_audio(self, file_path: str) -> str:
        """Transcribe a short audio file without chunking."""
        with open(file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript