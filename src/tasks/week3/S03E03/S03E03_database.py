from typing import List, Dict, Optional
import json
from src.clients.openai_client import OpenAIClient
from tasks.base_task import BaseTask
from src.tasks.week3.S03E03.generate_query_prompt import get_system_prompt


class Database(BaseTask):
    def __init__(self) -> None:
        super().__init__(task_name="database")
        self.ai_client = OpenAIClient()

    def get_table_names_list(self) -> List[str]:
        """
        Retrieve all table names from the database.
        
        Returns:
            List[str]: List of table names
        """
        query_result = self.client.get_database_query("SHOW TABLES")
        
        if not query_result or "reply" not in query_result:
            self.logger.error("Failed to retrieve table names")
            return []
        
        table_names = [table['Tables_in_banan'] for table in query_result["reply"]]
        self.logger.info(f"Retrieved {len(table_names)} tables")
        return table_names
    
    def get_table_schema(self, table_name: str) -> Optional[str]:
        """
        Retrieve schema for a specific table.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            Optional[str]: Table schema or None if not found
        """
        query = f"SHOW CREATE TABLE {table_name}"
        result = self.client.get_database_query(query)
        
        if not result or "reply" not in result or not result["reply"]:
            self.logger.error(f"Failed to retrieve schema for table: {table_name}")
            return None
            
        return result["reply"][0].get("Create Table")

    def collect_table_schemas(self, table_names: List[str]) -> Dict[str, str]:
        """
        Collect schemas for all specified tables.
        
        Args:
            table_names (List[str]): List of table names
            
        Returns:
            Dict[str, str]: Dictionary mapping table names to their schemas
        """
        table_schemas = {}
        
        for table_name in table_names:
            schema = self.get_table_schema(table_name)
            if schema:
                self.logger.info(f"Retrieved schema for table: {table_name}")
                table_schemas[table_name] = schema
            
        return table_schemas

    def execute_ai_query(self, question: str, system_prompt: str) -> List[str]:
        """
        Execute an AI-generated query based on the question.
        
        Args:
            question (str): Question to generate query for
            system_prompt (str): System prompt for the AI
            
        Returns:
            List[str]: List of datacenter IDs
        """
        answer = self.ai_client.answer_question(
            question=question,
            system_message=system_prompt
        )
        
        try:
            query = json.loads(answer).get("query", "")
            if not query:
                self.logger.error("Generated query is empty")
                return []
                
            results = self.client.get_database_query(query)
            return [result.get("dc_id") for result in results.get("reply", [])]
            
        except json.JSONDecodeError:
            self.logger.error("Failed to parse AI response as JSON")
            return []
    
    def process(self) -> List[str]:
        """
        Process the database query workflow.
        
        Returns:
            List[str]: List of active datacenter IDs
        """
        table_names = self.get_table_names_list()
        if not table_names:
            return []
            
        table_schemas = self.collect_table_schemas(table_names)
        if not table_schemas:
            return []
            
        system_prompt = get_system_prompt(table_schemas)
        question = "które aktywne datacenter (DC_ID) są zarządzane przez pracowników, którzy są na urlopie (is_active=0)"
        
        dc_ids = self.execute_ai_query(question, system_prompt)
        self.logger.info(f"Found {len(dc_ids)} matching datacenter IDs")
        
        return dc_ids
        

