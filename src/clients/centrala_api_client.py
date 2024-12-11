from urllib.parse import urljoin
import requests
import os
import json
from dotenv import load_dotenv

class CentralaAPIClient:
    def __init__(self, task_name, data_url=None):
        load_dotenv()
        self.api_key = os.getenv("POLIGON_API_KEY")
        self.task_name = task_name
        self.data_url = data_url
        self.base_url = os.getenv("CENTRALA_BASE_URL")

    def send_answer(self, answer, endpoint="/report"):
        self.url = urljoin(self.base_url, endpoint)
        """Sends answer to the verify URL."""
        payload = {
            "task": self.task_name,
            "apikey": self.api_key,
            "answer": answer
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, headers=headers, json=payload)
        return response.json()


    def get_database_query(self, query, task_name="database", endpoint="/apidb"):
        self.url = urljoin(self.base_url, endpoint)
        payload = {
            "task": task_name,
            "apikey": self.api_key,
            "query": query
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, headers=headers, json=payload)
        return response.json()