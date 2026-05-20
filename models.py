# todo/models.py

class Task:
    def __init__(self, task, priority=2, done=False,id=None):
        self.id = id
        self.task = task
        self.priority = priority
        self.done = done

    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task,
            "priority": self.priority,
            "done": self.done
        }
