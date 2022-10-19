from pydantic import BaseModel

class RoomCount(BaseModel):
    room: int
    count: int