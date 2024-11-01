from src.clients.openai_transcription_client import OpenAITranscriptionClient
import os  # Add this import at the top of your file

def main():
    audio_file_path = os.path.expanduser("~/Desktop/test.mp3")  # Expand the tilde to the full path
    transcription_client = OpenAITranscriptionClient()
    
    # Step 1: Chunk the audio file
    # chunks = transcription_client.chunk_audio(audio_file_path, chunk_duration=60)  # 60 seconds per chunk
    
    # Step 2: Transcribe the chunks
    transcription = transcription_client.transcribe_short_audio(audio_file_path)
    
    # Print the transcription result
    print(transcription)

if __name__ == "__main__":
    main() 