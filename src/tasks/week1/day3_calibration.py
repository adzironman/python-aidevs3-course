import json
from typing import Any, List, Dict

from src.clients.openai_client import OpenAIClient
from src.clients.poligon_api_client import PoligonAPIClient
from tasks.base_task import BaseTask

class Calibration(BaseTask):
    def __init__(self):
        super().__init__(task_name="JSON")
    
    whole_data: List[Dict[str, Any]] = []

    def fetch_data(self) -> List[Dict[str, Any]]:
        # Load the JSON data from the file
        with open('src/tasks/week1/calibration_data.json', 'r') as file:
            self.whole_data = json.load(file)
        return self.whole_data

    def filter_data(self, filter_key: str) -> List[Dict[str, Any]]:
        # Filter objects that have or not the field "test"
        if filter_key == 'test':
            filtered_data = [item for item in self.whole_data['test-data'] if 'test' in item]
        elif filter_key == 'math_only':
            filtered_data = [item for item in self.whole_data['test-data'] if not'test' in item]
        else:
            raise ValueError(f"Invalid filter key: {filter_key}")
        return filtered_data


    def check_math_actions(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for item in data:
            question = item['question']

            # Evaluate the mathematical expression
            actual_answer = eval(question)
            results.append({
                    "question": question,
                    "answer": actual_answer,
                })
        return results
    
    def check_test_elemets(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        openai_client = OpenAIClient()
        for item in data:
            math_question = item['question']
            actual_answer = eval(math_question)
            test_item = item['test']
            openai_response = openai_client.answer_question(test_item['q'])
            test_item['a'] = openai_response
            results.append({
                    "question": math_question,
                    "answer": actual_answer,
                    "test": item['test'],
            })
        return results

    def process(self, data: Any = None):
        self.fetch_data()
        fixed_data_with_math_only = self.check_math_actions(self.filter_data('math_only'))
        fixed_data_with_test = self.check_test_elemets(self.filter_data('test'))

        # Combine the two lists into one
        combined_data = fixed_data_with_math_only + fixed_data_with_test
        self.whole_data['test-data'] = combined_data
        
        return self.whole_data


