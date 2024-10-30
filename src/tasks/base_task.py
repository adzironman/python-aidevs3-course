from abc import ABC, abstractmethod
from src.clients.ai_devs_client import PoligonAPIClient
from typing import Any

class BaseTask(ABC):
    def __init__(self):
        self.client = self._create_client()

    @abstractmethod
    def _create_client(self) -> PoligonAPIClient:
        """Create specific client for the task"""
        pass

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process task-specific data"""
        pass

    def run(self):
        data = self.client.fetch_data()
        result = self.process(data)
        return self.client.send_answer(result) 