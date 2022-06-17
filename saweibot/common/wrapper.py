from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, final
from pydantic import BaseModel

from .redis import RedisObjFactory, RedisObjectBase, RedisJsonObject

WRAPPED_MODEL = TypeVar("WRAPPED_MODEL", bound=BaseModel)
PROXY_OBJECT = TypeVar("PROXY_OBJECT", bound=RedisObjectBase)

class BaseModelWrapper(Generic[PROXY_OBJECT], metaclass=ABCMeta):

    @final
    def factory(self, prefix: str=None):
        return RedisObjFactory(prefix=prefix)

    @property
    @final
    def proxy(self) -> PROXY_OBJECT:
        """
        Get proxy object from _proxy implement.
        """
        return self._proxy()

    # Deinfe how to get proxy object.
    @abstractmethod
    def _proxy(self): 
        raise NotImplementedError        

class StorageJsonModelWrapper(Generic[WRAPPED_MODEL], BaseModelWrapper[RedisJsonObject], metaclass=ABCMeta):
    
    __model__ : WRAPPED_MODEL

    def __init__(self):
        self.__data = None
        

    @final
    async def get_model(self, auto_save: bool = True) -> WRAPPED_MODEL:
        """
        """
        result = await self.load()
        if auto_save:
            await self.save_proxy()
        return result


    @final
    async def load(self) -> WRAPPED_MODEL:
        """
        """
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
        self.__data = self.__model__()
        return self.__data


    @final
    async def from_proxy(self) -> WRAPPED_MODEL:
        """
        Load data from redis proxy object.
        """
        return await self._from_proxy()

    @final
    async def from_db(self) -> WRAPPED_MODEL:
        """
        Load data from database.
        """
        return await self._from_db()

    @final
    async def save_proxy(self, data: WRAPPED_MODEL=None, **kwargs):
        """
        Save data with proxy boject.

        :params data[WRAPPED_MODEL]
        """
        data = data if data else (await self.load())
        await self._save_proxy(data, **kwargs)

    @final
    async def save_db(self, data: WRAPPED_MODEL=None, **kwargs):
        """
        Save data into database.

        :params data[WRAPPED_MODEL]
        """
        data = data if data else (await self.load())
        await self._save_db(data, **kwargs)

    # Define abstract load method.
    async def _from_proxy(self):
        return None
    
    async def _from_db(self):
        return None

    # Deinfe abstract save method.
    async def _save_proxy(self, data: WRAPPED_MODEL, **kwargs):
        raise NotImplementedError
    
    async def _save_db(self, data: WRAPPED_MODEL, **kwargs):
        raise NotImplementedError
