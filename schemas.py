# schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


        
        
class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # <-- Utilisez ceci à la place