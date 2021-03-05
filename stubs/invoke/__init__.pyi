from typing import Callable, Dict

class Collection:
    def add_task(self, task, name=None, aliases=None, default=None): ...

class Program: ...

class Task:
    body: Callable
    help: Dict

def task(*args, **kwargs): ...

class Context: ...
