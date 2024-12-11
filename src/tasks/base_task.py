from abc import ABC, abstractmethod

from src.clients.centrala_api_client import CentralaAPIClient
from typing import Any

from src.utils.logger_config import setup_logger


class BaseTask(ABC):
    def __init__(self, task_name):
        self.client = self._create_client(task_name)
        self.logger = setup_logger(f"Task:{task_name}")


    def _create_client(self, task_name) -> CentralaAPIClient:
        """Create specific client for the task"""
        return CentralaAPIClient(task_name=task_name)
        
    @abstractmethod
    def process(self) -> Any:
        """Process task-specific data"""
        pass

    def run(self):
        result = self.process()
        self.logger.info(f"Sending answer: {result}")
        response = self.client.send_answer(result) 
        self.logger.info(f"AI devs Centrala response: {response}")
        return response