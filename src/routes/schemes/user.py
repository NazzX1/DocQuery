from pydantic import BaseModel
from typing import Optional



class LoginRequest(BaseModel):
    email : str
    password : str


class RegisterRequest(BaseModel):
    username : str
    email : str
    password : str