import os
from typing import Any
from src.clients.openai_client import OpenAIClient
from src.clients.poligon_api_client import PoligonAPIClient
from src.tasks.base_task import BaseTask
from src.services.audio_files_service import get_all_file_paths, process_audio_transcription
from src.prompts.mp3_prompt import get_prompt

class Mp3(BaseTask):
    def _create_client(self) -> PoligonAPIClient:
        return PoligonAPIClient(
            task_name="mp3"
        )
    
    def fetch_data(self) -> Any:
        audio_files_paths = get_all_file_paths(os.path.expanduser("~/Desktop/audio"))
        audio_files_paths = [path for path in audio_files_paths if path.endswith('.m4a')]
        return audio_files_paths

    def process(self, data: Any) -> Any:
        transcription_files_paths = []
        # for audio_file_path in data:
        #     transcription_file_path = process_audio_transcription(audio_file_path, chunk_duration=100, output_file_name=f"{audio_file_path.split('.')[0]}.txt")
        #     transcription_files_paths.append(transcription_file_path)

        transcription_files_paths = ['/Users/adrianorszulik/Desktop/audio/michal.txt', '/Users/adrianorszulik/Desktop/audio/ardian.txt', '/Users/adrianorszulik/Desktop/audio/rafal.txt', '/Users/adrianorszulik/Desktop/audio/monika.txt', '/Users/adrianorszulik/Desktop/audio/agnieszka.txt', '/Users/adrianorszulik/Desktop/audio/adam.txt']
        
        # Create combined text with headers
        combined_text = ""
        for file_path in transcription_files_paths:
            # Extract filename without extension and path
            file_name = os.path.basename(file_path).replace('.txt', '')
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Add header and content to combined text
            combined_text += f"\n### {file_name.upper()} ###\n\n{content}\n\n"

        prompt = get_prompt(combined_text)

        #works also on model="gpt-4o-mini"
        openai_client = OpenAIClient()
        result = openai_client.answer_question(
            question=prompt, 
            model="gpt-4o", 
            response_format="json_object"
        )

        return result