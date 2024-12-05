from abc import ABC, abstractmethod
import logging
from venv import logger
from src.clients.poligon_api_client import PoligonAPIClient
from typing import Any

logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
logger = logging.getLogger(__name__) 

class BaseTaskPoligon(ABC):
    def __init__(self):
        self.client = self._create_client()

    @abstractmethod
    def _create_client(self) -> PoligonAPIClient:
        """Create specific client for the task"""
        pass

    @abstractmethod
    def process(self, data: Any = None) -> Any:
        """Process task-specific data"""
        pass

    @abstractmethod
    def fetch_data(self) -> Any:
        """Fetch task-specific data"""
        pass

    def run(self):
        data = self.fetch_data()
        logger.info(f"Fetched data: {data}")
        result = self.process(data)
        logger.info(f"Sending answer: {result}")
        response = self.client.send_answer(result) 
        logger.info(f"AI devs Centrala response: {response}")
        return response