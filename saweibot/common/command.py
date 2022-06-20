from typing import Any, List, Tuple

class CommandMap:

    def __init__(self, prefix='$'):
        self.prefix = prefix
        self.__handlers = dict()

    @property
    def handlers(self):
        return self.__handlers

    def register_command_handler(self, command: str, callback: Any):
        self.__handlers[command] = callback

    def register_command(self, command: str):
        def decreator(callback):
            self.register_command_handler(command, callback)
        return decreator

    def _command_split(self, text: str) -> Tuple[str, List[str]]:
        groups = text.strip().split()
        cmd = groups[0].lstrip('$')
        args = groups[1:]
        return cmd, args

    def is_avaliable(self, text: str):
        groups = text.strip().split()
        if not groups[0].startswith(self.prefix):
            return False
        cmd = groups[0].lstrip(self.prefix)
        return cmd in self.__handlers

    async def notify(self, text: str, **kwargs):
        cmd, cmd_args = self._command_split(text)
        handler = self.__handlers.get(cmd)
        if (handler):
            await handler(*cmd_args, **kwargs)