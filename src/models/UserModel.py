from .BaseDataModel import BaseDataModel
from .db_schemes import User
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from passlib.hash import bcrypt

class UserModel(BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_USERS_NAME.value]


    @classmethod
    async def create_instance(cls, db_client : object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance


    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_USERS_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_USERS_NAME.value]
            indexes = User.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name = index["name"],
                    unique = index["unique"]
                )


    async def register(self, user : User):


        existing_user = await self.collection.find_one({"email": user.email})
        if existing_user:
            return None
        
        user.password = bcrypt.hash(user.password)

        result = await self.collection.insert_one(user.dict(by_alias=True, exclude_unset=True))
        user.id = result.inserted_id
        return user
    
    
    
    async def login(self, email : str, password : str):

        record = await self.collection.find_one({
            "email" : email,
        })

        if not record:
            return None    

        # if not bcrypt.verify(password, record["password"]):
        #     return None
        
        return User(**record)