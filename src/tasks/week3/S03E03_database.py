from src.clients.openai_client import OpenAIClient
from src.tasks.base_task import BaseTask


class Database(BaseTask):
    def __init__(self):
        super().__init__(task_name="database")
        self.ai_client = OpenAIClient()

    def get_table_names_list(self) -> list[str]:
        # Get all tables from database
        all_tables = self.client.get_database_query("SHOW TABLES").get("reply", [])
        
        # Extract just the table names from the response
        table_names = [table['Tables_in_banan'] for table in all_tables]
        self.logger.info(f"Table names: {table_names}")
        return table_names
    
    def get_table_schema(self, table_name: str) -> dict:
        query = f"show create table {table_name}"
        table_schema = self.client.get_database_query(query).get("reply", [])
        return table_schema[0].get("Create Table", {})

    
    def process(self):
        table_names = self.get_table_names_list()
        table_schemas = {}

        for table_name in table_names:
            table_schema = self.get_table_schema(table_name)
            self.logger.info(f"Table schema:\n {table_schema}\n")
            table_schemas[table_name] = table_schema



