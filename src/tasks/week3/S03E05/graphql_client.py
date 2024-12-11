from neo4j import GraphDatabase
from src.tasks.week3.S03E05.models import Connection, User

uri = "neo4j://localhost:7687"
auth = ("neo4j", "test1234")

driver = GraphDatabase.driver(uri, auth=auth)

# define functions to interact with database
# those functions can be used by LLM as tools or manually to organize the data
def add_user_tx(tx, user: User):
    qry = """
    MERGE (u:User {
        id: $id,
        username: $username,
        accessLevel: $access_level,
        isActive: $is_active,
        lastlog: $lastlog
    })
    """
    return tx.run(
        qry, id=user.id, username=user.username, access_level=user.access_level,
        is_active=user.is_active, lastlog=user.lastlog
    )

def add_user_relationship(tx, user_a: int, user_b: int):
    qry = """
    MATCH (ua:User {id:$id_a})
    MATCH (ub:User {id:$id_b})
    MERGE (ua)-[r:KNOWS]->(ub)
    """
    return tx.run(qry, id_a=user_a, id_b=user_b)

# query the database to find the shortest path from user_a to user_b
def find_shortest_path_tx(tx, id_a: int, id_b: int):
    qry = """
    MATCH (ua:User {id: $id_a}), (ub:User {id: $id_b})
    MATCH p = shortestPath((ua)-[:KNOWS*]-(ub))
    RETURN p AS result
    """
    result = tx.run(qry, id_a=id_a, id_b=id_b)
    return result.single()

# add all users to database
def add_users_to_db(users: list[User]):
    with driver.session(database="neo4j") as session:
        for user in users:
            session.execute_write(add_user_tx, user=user)

# add user relationships to database
def add_user_relationships_to_db(connections: list[Connection]):
    with driver.session(database="neo4j") as session:
        for conn in connections:
            session.execute_write(add_user_relationship, user_a=conn.user1_id, user_b=conn.user2_id)


def find_shortest_path(user_a: int, user_b: int):
    with driver.session(database="neo4j") as session:
        result = session.execute_read(find_shortest_path_tx, id_a=user_a, id_b=user_b)
        if result is None:
            return None
        return result