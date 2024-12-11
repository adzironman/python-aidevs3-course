from pydantic import BaseModel


class Connection(BaseModel):
    user1_id: int
    user2_id: int

class User(BaseModel):
    id: int
    username: str
    access_level: str
    is_active: int
    lastlog: str