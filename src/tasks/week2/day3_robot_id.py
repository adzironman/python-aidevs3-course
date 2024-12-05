import json
import os
import requests
from src.clients.openai_client import OpenAIClient
from src.clients.poligon_api_client import PoligonAPIClient
from src.tasks.base_task_v2 import BaseTaskV2



class RobotId(BaseTaskV2):
    def __init__(self):
        super().__init__(task_name="robotid")

    def fetch_data(self) -> str:
        env_key = os.getenv("POLIGON_API_KEY")
        url = "https://centrala.ag3nts.org/data/KLUCZ-API/robotid.json".replace("KLUCZ-API", env_key)
        response = requests.get(url)
        return response.text
    
    def process(self) -> str:
        data = self.fetch_data()
        description = json.loads(data).get("description")
        self.logger.info(f"Initial Description: {description}")

        openai_client = OpenAIClient()
        response = openai_client.answer_question(description, system_message="Popraw otrzymany opis robota. Zrób to w taki sposób, żeby było to zrozumiałe dla modelu Dall-E do tworzenia obrazów.")
        self.logger.info(f"Processed Description: {response}")

        image = openai_client.generate_image(response)
        self.logger.info(f"Generated Image: {image}")

        return image