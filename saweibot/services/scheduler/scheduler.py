from datetime import timedelta
from time import time
from sanic import Sanic
from typing import Callable, Mapping, Optional, Union

class AppScheduleTask:
    
    def __init__(self, callback: Callable, 
                       period: Optional[timedelta],
                       start_time:Optional[Union[timedelta, time]],
                       app: Sanic):
        self.callback = callback
        self.period = period
        self.start_time = start_time
        self.app = app

    def __get_next_run():
        pass

    async def run(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass



class AppScheduler:
    
    def __init__(self, app: Sanic=None):
        self.app = app
        self._registerd_task: Mapping[str, AppScheduleTask] = []

    def register_task_handler(self, name: str, func: Callable):
        self._registerd_task[name] = AppScheduleTask(func=func)
    
    def register_task(self):
        def wrapper(callback):
            return callback
        return wrapper

    async def run_scheduler(self, app: Sanic, loop):
        for task in self.__registerd_task:
            pass
    
    async def stop_scheduler(self, app: Sanic, loop):
        for job in self.jobs.values():
            await job.stop()