import functools
import inspect
from types import FunctionType
from typing import no_type_check_decorator

from invoke import Collection, Task, task


def partial(t1: Task, **new_defaults):
    @no_type_check_decorator
    @functools.wraps(t1.body)
    def partial_task(c, **original_params) -> FunctionType:
        partially_applied_params = {}
        partially_applied_params.update(original_params)
        partially_applied_params.update(new_defaults)
        return t1.body(c, **partially_applied_params)

    # Had to ignore mypy due to https://github.com/python/typing/issues/598
    # And https://github.com/python/mypy/issues/5958
    partial_task.__signature__ = inspect.signature(t1.body)  # type: ignore
    t2 = task(
        partial_task,
        help={k: v for k, v in t1.help.items() if k not in new_defaults},
    )
    t2.__doc__ = t1.__doc__
    return t2


def add_task(ns: Collection, t: Task, **kwargs):
    t2 = partial(t, **kwargs)
    ns.add_task(t2)
