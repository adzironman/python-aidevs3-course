import os
import requests


class JinaEmbeddingClient:
    def __init__(self):
        self.JINA_API_KEY = os.getenv("JINA_API_KEY")

    def create_jina_embedding(self, text: str) -> list[float]:
        url = 'https://api.jina.ai/v1/embeddings'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.JINA_API_KEY}'
        }
        payload = {
            'model': 'jina-embeddings-v3',
            'task': 'text-matching',
            'dimensions': 1024,
            'late_chunking': False,
            'embedding_type': 'float',
            'input': [text]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                raise Exception(f"HTTP error! Status: {response.status_code}")
            
            data = response.json()
            return data['data'][0]['embedding']
        except Exception as error:
            print("Error creating Jina embedding:", error)
            raise error
