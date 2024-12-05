import json
import os
from src.tasks.week2.categoization_text_prompt import get_prompt
from src.clients.openai_client import OpenAIClient
from src.clients.poligon_api_client import PoligonAPIClient
from src.tasks.base_task_v2 import BaseTaskV2
from src.services.audio_files_service import get_all_file_paths, process_audio_transcription


class Category(BaseTaskV2):
    def __init__(self) -> None:
        self.people_related_files: list[str] = []
        self.hardware_related_files: list[str] = []
        super().__init__(task_name="kategorie")
    
    def fetch_data(self) -> tuple[list[str], list[str], list[str]]:
        all_files_paths = get_all_file_paths(os.path.expanduser("~/Desktop/dev_materials/ai_devs3/pliki_z_fabryki"))
        audio_files_paths = [path for path in all_files_paths if path.endswith('.mp3')]
        txt_files_paths = [path for path in all_files_paths if path.endswith('.txt')]
        png_files_paths = [path for path in all_files_paths if path.endswith('.png')]

        return (audio_files_paths, txt_files_paths, png_files_paths)

    def process_audio_files(self, audio_files_paths: list[str]) -> None:

        self.logger.info(f"Processing {len(audio_files_paths)} audio files")
        for audio_file_path in audio_files_paths:
            transcription = process_audio_transcription(audio_file_path, chunk_duration=100, output_file_name=f"{audio_file_path.split('/')[-1].split('.')[0]}.txt")
            category = self._get_category(transcription)
            self._save_category(category, audio_file_path)


    def process_txt_files(self, txt_files_paths: list[str]) -> None:
        self.logger.info(f"Processing {len(txt_files_paths)} txt files")
        for txt_file_path in txt_files_paths:
            with open(txt_file_path, "r") as file:
                transcription = file.read()
            category = self._get_category(transcription)
            self._save_category(category, txt_file_path)

    def process_png_files(self, png_files_paths: list[str]) -> None:
        openai_client = OpenAIClient()
        self.logger.info(f"Processing {len(png_files_paths)} png files")
        for png_file_path in png_files_paths:
            text = openai_client.read_text_from_image(png_file_path)
            category = self._get_category(text)
            self._save_category(category, png_file_path)


    def _get_category(self, transcription: str) -> str:
        openai_client = OpenAIClient()
        system_prompt = get_prompt()
        answer = openai_client.answer_question(transcription, system_message=system_prompt, response_format="json_object")
        self.logger.info(f"Answer: {answer}")
        return json.loads(answer)["category"]
    
    def _save_category(self, category: str, file_path: str) -> None:
        file_name = file_path.split('/')[-1]
        if category == "PEOPLE":
            self.logger.info(f"People related file: {file_name}")
            self.people_related_files.append(file_name)
        elif category == "HARDWARE":
            self.logger.info(f"Hardware related file: {file_name}")
            self.hardware_related_files.append(file_name)

    def process(self) -> dict[str, list[str]]:
        data = self.fetch_data()
        # self.process_audio_files(data[0])
        # self.process_txt_files(data[1])
        # self.process_png_files(data[2])
        self.logger.info(f"People related files: {self.people_related_files}")
        self.logger.info(f"Hardware related files: {self.hardware_related_files}")  

        return {

        "people": ['2024-11-12_report-10-sektor-C1.mp3', '2024-11-12_report-00-sektor_C4.txt', '2024-11-12_report-07-sektor_C4.txt'], 
        "hardware": ['2024-11-12_report-13.png', '2024-11-12_report-15.png', '2024-11-12_report-17.png']} 
        # return {
        #     "people": self.people_related_files,
        #     "hardware": self.hardware_related_files
        # }

#'2024-11-12_report-12-sektor_A1.mp3', 


