# src/services/drone_service.py
from typing import Optional
from venv import logger
from src.clients.openai_client import OpenAIClient
from src.tasks.week4.S04E04.config import Config
from src.tasks.week4.S04E04.grid_navigation_prompt import get_grid_navigation_prompt

class DroneNavigator:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.config = Config()
        self.map_description = self.config.MAP_DESCRIPTION
    
    def navigate(self, instruction: str) -> Optional[str]:
        """
        Navigate the drone based on the given instruction.
        
        Args:
            instruction: Navigation instruction
            
        Returns:
            Optional[str]: Terrain description or None if not found
        """
        try:
            response = self.openai_client.answer_question(
                question=instruction,
                system_message=get_grid_navigation_prompt()
            )

            return self.map_description.get(response)
        except Exception as e:
            logger.error(f"Navigation error: {str(e)}")
            raise