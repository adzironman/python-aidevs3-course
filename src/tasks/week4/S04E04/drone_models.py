# src/models/drone_models.py
from pydantic import BaseModel

class DroneInstruction(BaseModel):
    instruction: str

class DroneResponse(BaseModel):
    description: str