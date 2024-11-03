from src.tasks.base_task import BaseTask
from src.clients.poligon_api_client import PoligonAPIClient

class PoligonTask(BaseTask):
    def _create_client(self) -> PoligonAPIClient:
        return PoligonAPIClient(
            task_name="POLIGON",
            data_url="https://poligon.aidevs.pl/dane.txt"
        )

    def process(self, data):
        # Poligon-specific data processing logic
        client = self._create_client()
        data = client.fetch_data()

        # Split the data into a list of strings
        result = data.text.strip().split('\n')
        print(result)

        return result

