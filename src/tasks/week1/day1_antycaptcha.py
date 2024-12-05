from src.clients.openai_client import OpenAIClient
from tasks.base_task import BaseTask
from bs4 import BeautifulSoup
import requests  # Make sure to import requests for fetching HTML


class AntyCaptcha(BaseTask):
    def __init__(self):
        super().__init__(task_name="ANTYCAPTCHA")

    

    def process(self, data):
        url = "https://xyz.ag3nts.org/"
        username = "tester"
        password =  "574e112a"

        captcha_question = self.find_captcha_question(url)
        print(captcha_question)

        openai_client = OpenAIClient()
        answer = openai_client.answer_captcha_question(captcha_question)
        print(answer)

        response = requests.post(url, data={"username": username, "password": password, "answer": answer})
        print(response.text)

    def find_captcha_question(self, url: str) -> str:
        response = requests.get(url)  # Fetch the HTML source
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML
        question_element = soup.find(id="human-question")  # Find the element by ID
        return question_element.text if question_element else "Element not found"  # Return the text or a message
    
