import requests
import os
import json
from dotenv import load_dotenv

class PoligonAPIClient:
    def __init__(self, task_name, data_url=None):
        load_dotenv()
        self.api_key = os.getenv("POLIGON_API_KEY")
        self.task_name = task_name
        self.data_url = data_url
        self.verify_url = "https://poligon.aidevs.pl/verify"

    def fetch_data(self):
        """Fetches data from the data URL."""
        if not self.data_url:
            return None
        
        response = requests.get(self.data_url)
        response.raise_for_status()
        return response # or response.text depending on your needs

    def send_answer(self, answer):
        """Sends answer to the verify URL."""
        payload = {
            "task": self.task_name,
            "apikey": self.api_key,
            "answer": answer
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.verify_url, headers=headers, json=payload)
        return response.json()
