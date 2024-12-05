
import os
from typing import Any, Dict

from dotenv import load_dotenv
from src.clients.openai_client import OpenAIClient
from src.clients.poligon_api_client import PoligonAPIClient
from src.tasks.base_task import BaseTask
from src.utils.http_util import HttpUtil, ResponseType
from src.utils.zip_util import ZipUtil

load_dotenv()
base_url = os.getenv('CENTRALA_BASE_URL')

class Documents(BaseTask):
    def __init__(self):
        super().__init__(task_name="dokumenty")

    
    def process(self) -> Any:
        self.logger.info("Starting processing documents")

        http_util = HttpUtil(base_url)
        response = http_util.getData(f"/dane/pliki_z_fabryki.zip", ResponseType.CONTENT)
        files = ZipUtil().extract_to_memory(response)

        self.logger.info(f"Extracted files: {files}")
        self.persons = self.get_persons_info(files)
        self.logger.info(f"persons: {self.persons}")

        files_keywords = self.get_reports_keywords(files)
        self.logger.info(f"files_keywords: {files_keywords}")

        self.fill_keywords_from_person_info(files_keywords)
        return files_keywords


    
    def get_persons_info(self, files) -> Dict[str,str] :
        result = {}
        for file_name, content in files.items():
            if not (file_name.endswith(".txt") and file_name.startswith("facts/")):
                continue

            if isinstance(content, bytes):
                content = content.decode('utf-8')

            if content.startswith("entry deleted"):
                continue

            prompt = f"""
            Your task is to check who is below description about.
            The name of the person is at the beginning of the description.
            Return name surname or only name if surname not exists.
            
            <description>
            {content}
            </description>
            """
            name = OpenAIClient().answer_question(prompt)
            result[name.lower()] = content
            self.logger.info(f"name from {file_name}: {name}")

        return result


    def fill_keywords_from_person_info(self, files_keywords):
        for report_name in files_keywords:
            name = files_keywords[report_name].split(",")[0]
            name = name.lower()
            self.logger.info(f"name: {name}")

            if name not in self.persons:
                continue

            person_info = self.persons[name]

            if person_info:
                self.logger.info(f"person_info founded for: {name}")
                person_keywords = self.get_person_keywords(person_info)
                self.logger.info(f"person_keywords: {person_keywords}")
                files_keywords[report_name] = files_keywords[report_name] + ", " + person_keywords


    def get_reports_keywords(self, files) -> Dict[str,str]:
        result = {}
        for file_name, content in files.items():
            if not file_name.endswith(".txt") or file_name.startswith("facts/"):
                continue

            if isinstance(content, bytes):
                content = content.decode('utf-8')

            prompt = f"""
            Your task is to find main keywords in below report.
            Return only keywords (in polish) separated with commas without any additional formating.
            
            <rules>
            - Add sector name from report name to keywords
            - SEARCH keywords carefully in report
            - WHEN you find person name in report, return as first keyword
            - Return keywords in denominator
            - Never return "\n" line in keywords
            </rules>
            
            <report>
            report name: {file_name}
            report content: {content}
            </report>
            
            """
            keywords = OpenAIClient().answer_question(prompt, temperature=0.7)
            keywords = keywords.replace("\n", "")
            result[file_name] = keywords
            self.logger.info(f"keywords from {file_name}: {keywords}")

        return result

    def get_person_keywords(self, content):
        prompt = f"""
            Your task is to find main keywords in below context.
            Return only keywords (in polish) separated with commas without any additional formating.
            
            <rules>
            - Return keywords in denominator
            - WHEN you find person name in context, return as first keyword
            </rules>
       
            <context>
            {content}
            </context>
            """
        keywords = OpenAIClient().answer_question(prompt)
        return keywords
                         