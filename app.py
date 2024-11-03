from src.services.audio_files_service import process_audio_transcription
import os

def main():
    process_audio_transcription(os.path.expanduser("")) #e.g."~/Desktop/test.mp3"

if __name__ == "__main__":
    main() 