from pydantic import BaseModel

class TableRegister(BaseModel):
    seats: int

class SavePositions(BaseModel):
    table_id: str
    position_x: float
    position_y: float
