import json
import os
import requests
from src.clients.openai_client import OpenAIClient
from src.clients.poligon_api_client import PoligonAPIClient
from src.tasks.base_task import BaseTask
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobotId(BaseTask):
    def _create_client(self) -> PoligonAPIClient:
        return PoligonAPIClient(
            task_name="robotid"
        )

    def fetch_data(self) -> str:
        env_key = os.getenv("POLIGON_API_KEY")
        url = "https://centrala.ag3nts.org/data/KLUCZ-API/robotid.json".replace("KLUCZ-API", env_key)
        response = requests.get(url)
        return response.text
    
    def process(self, data: str) -> str:
        description = json.loads(data).get("description")
        logger.info(f"Initial Description: {description}")

        openai_client = OpenAIClient()
        response = openai_client.answer_question(description, system_message="Popraw otrzymany opis robota. Zrób to w taki sposób, żeby było to zrozumiałe dla modelu Dall-E do tworzenia obrazów.")
        logger.info(f"Processed Description: {response}")

        image = openai_client.generate_image(response)
        logger.info(f"Generated Image: {image}")

        return image

