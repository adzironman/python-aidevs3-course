from src.clients.openai_client import OpenAIClient
import os
from pydub import AudioSegment
from typing import List


def chunk_audio(file_path: str, chunk_duration: int = 60) -> List[str]:
    """Chunk audio file into smaller parts."""
    audio_chunks = []
    audio = AudioSegment.from_file(file_path)  # Load the audio file
    total_length = len(audio)  # Length in milliseconds
    chunk_size = chunk_duration * 1000  # Convert seconds to milliseconds

    for start in range(0, total_length, chunk_size):
        chunk = audio[start:start + chunk_size]
        chunk_file_path = f"chunk_{start // chunk_size}.wav"
        chunk.export(chunk_file_path, format="wav")  # Export as WAV
        audio_chunks.append(chunk_file_path)

    return audio_chunks


def process_audio_transcription(audio_file_path: str, chunk_duration: int = 200, output_file_name: str = "transcription_result.txt") -> str:
    transcription_client = OpenAIClient()
    
    # Step 1: Chunk the audio file
    chunks = chunk_audio(audio_file_path, chunk_duration=chunk_duration)
    
    # Step 2: Transcribe the chunks
    transcription = transcription_client.transcribe_audio(chunks)
    
    # Define the output directory relative to the repository root
    output_directory = os.path.join(os.path.dirname(__file__), '../output')
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Specify the output file path
    output_file_path = os.path.join(output_directory, output_file_name)  # Create the file path
    with open(output_file_path, 'w') as output_file:  # Open the file in write mode
        output_file.write(transcription)  # Write the transcription to the file

    return transcription


def get_all_file_paths(directory: str) -> List[str]:
    """Retrieve all file paths from the specified directory."""
    return [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]