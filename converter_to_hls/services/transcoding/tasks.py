import uuid
from abc import ABC, abstractmethod
from enum import Enum, auto


class State(Enum):
    IN_PROGRESS = auto()
    FINISHED_SUCCESSFULLY = auto()
    FINISHED_WITH_ERROR = auto()
    FAILED_TO_START = auto()

    def __str__(self):
        return self.name.lower()


class Task(ABC):
    def __init__(self):
        self._task_id = self.build_task_id()

    def build_task_id(self):
        return str(uuid.uuid4())

    @property
    def task_id(self):
        return self._task_id

    def __eq__(self, other):
        return isinstance(other, Task) and self.task_id == other.task_id

    def __hash__(self):
        return hash(self.task_id)

    @property
    @abstractmethod
    def state(self):
        pass

    @abstractmethod
    async def run(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @property
    @abstractmethod
    def result(self):
        pass
