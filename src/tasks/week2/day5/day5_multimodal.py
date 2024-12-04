import os
import pathlib
import requests
from src.clients.poligon_api_client import PoligonAPIClient
from src.tasks.base_task import BaseTask


class MultimodalTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.context = None
        self.questions = None

    def _create_client(self) -> PoligonAPIClient:
        return PoligonAPIClient(
            task_name="arxiv"
        )

    def load_context(self) -> str:
        """Load and return the contents of the context.md file."""
        current_dir = pathlib.Path(__file__).parent
        context_path = current_dir / "context.md"
        
        try:
            with open(context_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Context file not found at {context_path}")
        except Exception as e:
            raise Exception(f"Error reading context file: {str(e)}")

    def fetch_data(self) -> None:
        self.context = self.load_context()


    def process(self, data: str) -> None:
        env_key = os.getenv("POLIGON_API_KEY")
        url = "https://centrala.ag3nts.org/data/KLUCZ-API/arxiv.txt".replace("KLUCZ-API", env_key)
        response = requests.get(url)
        print(response.text)

    def get_main_prompt(self, publication):
        prompt = f"""
        You have provided fictitious publication in markdown format and questions (both in polish).
        Your task is to find answer or relevant text/link, which can help answer specific questions,
        based only on provided publication.
       
        <rules>
        - Relevant link could be image link or audio link
        - ALWAYS use whole markdown link
        - Relevant text may be scattered throughout whole publication
        - COMBINING sentences or phrases in relevant text is allowed
        - ADD to text field EVERY publication fragment that could help in response to question
        - Information needed for questions could be included in attached image or audio 
        - FILL keywords (important names, phrases) based on text in text_keywords field
        - Find links based on text and text_keywords
        - OMIT link in text field
        - UNDER NO CIRCUMSTANCES use same link for different questions
        - Search MOST LIKELY answer in whole publication
        - Answer the question exactly as asked, stay on topic
        - WHEN answer for question NOT EXISTS, leave answer field EMPTY
        - WHEN answer is empty, it is MANDATORY to FIND link.
    
        </rules>
        
        <response-format>
        Return relevant elements in json format 
        {{"result":[{{"questionId":"question id","answer":"one sentence answer", "text":"relevant text",
         "text_keywords":"list of keywords","link":"relevant link or empty string"}}]}}
        </response-format>
        
        <steps>
        - Read whole publication and questions carefully 
        - Answer questions if possible
        - Find relevant text/link for each question
        - Verify that selected links are most appropriate for specific questions
        - Verify not repeating link across questions
        </steps>
        
        <questions>
        {self.questions}
        </questions>
        
        <publication>
        {publication}
        </publication>
        
        """
        return prompt

    