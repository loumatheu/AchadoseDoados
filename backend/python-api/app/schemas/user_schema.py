from typing import Optional
from pydantic import BaseModel as SCBaseModel

class UserSchema(SCBaseModel):
    id: Optional[int]
    username: str
    name: str
    email: str
    address: Optional[str] = None
    phone: Optional[str] = None
    password: str
    
    class Config:
        orm_mode = True