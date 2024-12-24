from pydantic import BaseModel, ConfigDict
from typing import Optional

class User(BaseModel):
    name: str
    last_name: str
    age: int
    email: str
    username: str
    password: str
    address: Optional[str] = None


class ShowUser(BaseModel):
    id: int
    username: str
    name: str
    last_name: str
    model_config = ConfigDict(from_attributes=True)



class UpdateUser(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None

class Login(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: str = None