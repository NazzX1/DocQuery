from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId
from typing import Optional

class User(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    username : str = Field(..., min_length=1)
    email : str = Field(..., min_length=1)
    password : str = Field(..., min_length=1)


    class Config:
         arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
         
         return [
              {
                   "key" : [
                        ("email", 1)
                   ],
                   "name" : "email_index_1",
                   "unique" : False

              }
         ]