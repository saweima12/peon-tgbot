from pydantic import BaseModel
from saweibot.storages.redis import RedisObjFactory
from typing import TypeVar, Type

class BaseModelWrapper():

    __model__ = BaseModel
    
    def __init__(self):
        self.__data = None

    def factory(self, prefix: str=None):
        return RedisObjFactory(prefix=prefix)

    async def get_model(self, auto_save: bool = True):

        result = await self.load()        

        if auto_save:
            await self.save()

        return result


    async def load(self):

        if self.__data:
            return self.__data

        # from proxy
        self.__data = await self.from_proxy()
        if self.__data:
            return self.__data
        
        # from db
        self.__data = await self.from_db()
        if self.__data:
            return self.__data
                
        # default
        self.__data = self.__model__()
        return self.__data

    @property
    def proxy(self):
        raise NotImplementedError

    async def from_proxy(self):
        raise NotImplementedError

    async def from_db(self):
        raise NotImplementedError

    async def save(self, data, **kwargs):
        raise NotImplementedError
        
    async def save_db(self, data, *args, **kwargs):
        raise NotImplementedError