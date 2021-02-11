import functools
import inspect
from invoke import Collection, Task, task


def partial(t1: Task, **new_defaults):
    @functools.wraps(t1.body)
    def partial_task(c, **original_params):
        partially_applied_params = {}
        partially_applied_params.update(original_params)
        partially_applied_params.update(new_defaults)
        return t1.body(c, **partially_applied_params)

    partial_task.__signature__ = inspect.signature(t1.body)
    t2 = task(
        partial_task,
        help={k: v for k, v in t1.help.items() if k not in new_defaults},
    )
    t2.__doc__ = t1.__doc__
    return t2


def add_task(ns: Collection, t: Task, **kwargs):
    t2 = partial(t, **kwargs)
    ns.add_task(t2)
