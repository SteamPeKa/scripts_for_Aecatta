# coding=utf-8
# Creation date: 08 дек. 2020
# Creation time: 14:07
# Creator: SteamPeKa

from typing import Iterable as _Iterable
from typing import Sized as _Sized


class SimpleTask(object):
    def __init__(self, USE_task_key, task_bank_key):
        self.__USE_task_key = str(USE_task_key)
        self.__task_bank_key = str(task_bank_key)

    @property
    def USE_task_key(self):
        try:
            USE_task_num = int(self.__USE_task_key)
        except ValueError:
            USE_task_num = self.__USE_task_key
        return USE_task_num

    @property
    def task_bank_key(self):
        try:
            task_bank_num = int(self.__task_bank_key)
        except ValueError:
            task_bank_num = self.__task_bank_key
        return task_bank_num

    def __hash__(self):
        return hash((self.USE_task_key, self.task_bank_key))

    def __eq__(self, other):
        if isinstance(other, SimpleTask):
            if self.USE_task_key == other.USE_task_key:
                if self.task_bank_key == other.task_bank_key:
                    return True
        return False

    def __cmp__(self, other):
        if isinstance(other, SimpleTask):
            if self.USE_task_key < other.USE_task_key:
                return -1
            elif self.USE_task_key > other.USE_task_key:
                return 1
            else:
                if self.task_bank_key < other.task_bank_key:
                    return -1
                elif self.task_bank_key > other.task_bank_key:
                    return 1
                else:
                    assert self == other
                    return 0
        else:
            raise ValueError("Type {} and type {} is not comparable".format(
                type(self),
                type(other)
            ))

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        if self == other:
            return True
        else:
            return self.__lt__(other)

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        if self == other:
            return True
        else:
            return self.__gt__(other)


class TaskBatch(_Iterable[SimpleTask], _Sized):
    def __init__(self):
        self.__tasks = set()

    def add_task(self, task: SimpleTask):
        if not isinstance(task, SimpleTask):
            raise ValueError("Can't add object of class {} to the {} object".format(type(task),
                                                                                    type(self)))
        if task not in self.__tasks:
            self.__tasks.add(task)
            return True
        else:
            return False

    def add_task_by_pair(self, USE_task_key, task_bank_key):
        return self.add_task(SimpleTask(USE_task_key=USE_task_key,
                                        task_bank_key=task_bank_key))

    def add(self, *args):
        if len(args) == 1:
            return self.add_task(args[0])
        elif len(args) == 2:
            return self.add_task_by_pair(*args)
        else:
            raise ValueError("Unresolved function call: {}.add({})".format(
                type(self),
                ", ".join("{{{}}}>:{}".format(repr(a), type(a)) for a in args)
            ))

    def update(self, iterable):
        if isinstance(iterable, _Iterable):
            return [self.add(args) if isinstance(args, SimpleTask) else self.add(*args) for args in iterable]
        else:
            raise ValueError("Unresolved function call: {}.update({{{}}}:{})".format(
                type(self),
                repr(iterable),
                type(iterable)
            ))

    def __iter__(self):
        return iter(sorted(list(self.__tasks)))

    def __len__(self):
        return len(self.__tasks)
