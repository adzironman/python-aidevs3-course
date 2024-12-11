import os
from src.tasks.base_task import BaseTask
from src.tasks.week3.S03E05.graphql_client import add_user_relationships_to_db, add_users_to_db, find_shortest_path
from src.tasks.week3.S03E05.models import Connection, User

db_url = f"{os.environ.get("CENTRALA_BASE_URL")}/apidb"
api_key = os.environ.get("POLIGON_API_KEY")




class GraphDbTask(BaseTask):
    def __init__(self):
        super().__init__(task_name="connections")
        
    def query_db(self, query: str):
        return self.client.get_database_query(query)

    def process(self):
        self.connections_db = self.client.get_database_query("select * from connections")
        connections = [Connection(**conn) for conn in self.connections_db["reply"]]
        self.users_db = self.query_db("select * from users")
        users = [User(**user) for user in self.users_db["reply"]]

        self.logger.info(f"Connections: {connections}")
        self.logger.info(f"Users: {users}")

        add_users_to_db(users)
        add_user_relationships_to_db(connections)

        user_a = list(filter(lambda user: user.username == "Rafał", users))[0]
        user_b = list(filter(lambda user: user.username == "Barbara", users))[0]

        path = find_shortest_path(user_a.id, user_b.id)
        self.logger.info(f"Shortest path: {path}")

        answer_a = ", ".join([
            item[1]
            for node in path["result"].nodes
            for item in node.items()
            if item[0] == "username"
        ])

        return answer_a


    










