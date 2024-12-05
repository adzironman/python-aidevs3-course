import os
from typing import Any
from openai import OpenAI
import requests
from src.tasks.base_task import BaseTask


class   Censure(BaseTask):
    def __init__(self):
        super().__init__(task_name="CENZURA")
    
    system_prompt = """
        <context>Twoim zadaniem jest zacenzurowanie tekstu. Kazdy osobisty detal zamieniusz na CENZURA.</context>
        <task>Zacenzuruj tekst. Kazdy osobisty detal zamieniusz na CENZURA (np. imie, nazwisko, adres, email, itp.). Zachowaj formatowanie tekstu i interpunkcje. Jeśli dwa cenzurowane wyrazy znajdują się obok siebie, zastąp je jednym słowem "CENZURA"</task>

        <examples>
        input1=Informacje o podejrzanym: Marek Jankowski. Mieszka w Białymstoku na ulicy Lipowej 9. Wiek: 26 lat.
        output1=Informacje o podejrzanym: CENZURA.  Mieszka w CENZURA na ulicy CENZURA. Wiek: CENZURA lat.
        </examples>

        <return> Zwróć ten sam tekst, z cenzurą. Nic więcej </return>
        """
    
    def fetch_data(self) -> Any:
        env_key = os.getenv("POLIGON_API_KEY")
        url = "https://centrala.ag3nts.org/data/KLUCZ/cenzura.txt".replace("KLUCZ", env_key)
        response = requests.get(url)
        return response.text
        
    
    # def process(self, data: Any) -> Any:
    #     openai_client = OpenAIClient()
    #     response = openai_client.answer_question(data, system_message=self.system_prompt)
    #     print(response)
    #     return response
    
    def process(self, data: Any) -> Any:
        clien = OpenAI (
            base_url="http://localhost:11434/v1",
            api_key='ollama' #required but unused
        )
        model_to_use = "llama2"

        response = clien.chat.completions.create(
            model=model_to_use,
            messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": data}],
            stream=False
        )
        print(response)
        return response

