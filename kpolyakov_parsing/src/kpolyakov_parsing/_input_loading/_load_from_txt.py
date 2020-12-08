# coding=utf-8
# Creation date: 08 дек. 2020
# Creation time: 13:55
# Creator: SteamPeKa

from ._objects import TaskBatch, SimpleTask

"""
Data sample:
25
7 11 28 31 50 67

11
6 10 81 25 61 13 79
"""


def load_from_txt(path=None, file=None):
    if path is None and file is None:
        raise ValueError("path argument xor file argument have to be specified")
    elif path is not None and file is None:
        with open(path, "r") as f:
            result = _load_from_opened_file(f)
        return result
    elif path is None and file is not None:
        return _load_from_opened_file(file)
    else:
        raise ValueError("path argument xor file argument have to be specified")


def _load_from_opened_file(opened_file):
    state = "waiting_USE_task_key"
    use_task_key = None
    result = TaskBatch()
    for line in opened_file:
        line = line.replace("\n", "")
        if state == "waiting_USE_task_key":
            assert use_task_key is None
            use_task_key = line
            state = "waiting_task_bank_keys"
        elif state == "waiting_task_bank_keys":
            for task_bank_key in line.split(" "):
                assert use_task_key is not None
                result.add(SimpleTask(use_task_key, task_bank_key))
            state = "waiting_end"
            use_task_key = None
        elif state == "waiting_end":
            use_task_key = None
            state = "waiting_USE_task_key"
    assert state in {"waiting_end", "waiting_USE_task_key"}
    return result
