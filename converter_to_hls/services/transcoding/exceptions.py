class ConverterException(Exception):
    def __init__(self, *args, task_id):
        self.task_id = task_id
        super().__init__(*args)


class DuplicatedTasksException(ConverterException):
    def __str__(self):
        return f'Task already exists. Task id: {self.task_id}.'


class LimitExceededException(ConverterException):
    def __init__(self, *args, limit, task_id=None):
        self.limit = limit
        super().__init__(*args, task_id=task_id)

    def __str__(self):
        return f'Running tasks limit exceeded. Limit: {self.limit}.'


class FailedToStartConvertation(ConverterException):
    def __str__(self):
        return f'Failed to start convertation.'
