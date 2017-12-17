import asyncio
from concurrent.futures import ThreadPoolExecutor

from .converter import ConvertTask, State
from .exceptions import LimitExceededException, DuplicatedTasksException


class ConvertManager:
    def __init__(self, config, loop=None):
        self.config = config
        self.loop = loop or asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=self.config['tasks_limit'])
        # TODO: replace with something like TasksRegistry
        self.tasks = {}

    async def convert(self, filename):
        convert_task = ConvertTask(filename, self.config, self.loop, self.executor)
        self[convert_task.task_id] = convert_task
        await convert_task.run()
        return convert_task

    def __setitem__(self, task_id, task):
        if self.limit_exceeded:
            raise LimitExceededException(limit=self.config['tasks_limit'])
        if task_id in self.tasks:
            raise DuplicatedTasksException(task_id=task_id)
        self.tasks[task_id] = task

    @property
    def limit_exceeded(self):
        return self.running_count + 1 > self.config['tasks_limit']

    @property
    def running_count(self):
        return sum(1 for c in self.tasks.values() if c.state == State.RUNNING)

    def __getitem__(self, task_id):
        return self.tasks[task_id]

    def __len__(self):
        return len(self.tasks)
