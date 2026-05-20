# todo/service.py

from models import Task
from storage import load, save


class ToDoService:
    def __init__(self):
        self.tasks = [Task(**t) for t in load()]
        self.next_id= self._get_next_id()

    def _get_next_id(self):
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, task, priority):
        new_task = Task(task, priority, id=self.next_id)
        self.next_id += 1
        self.tasks.append(new_task)
        save([t.to_dict() for t in self.tasks])

    def get_tasks(self, done: bool = None, priority: int = None):
        if done is None and priority is None:
            return [t.to_dict() for t in self.tasks]
        filtered_tasks = [t for t in self.tasks if (done is None or t.done == done) and (priority is None or t.priority == priority)]
        return [
                t.to_dict()
                for t in sorted(filtered_tasks, key=lambda x: (x.done, x.priority))
]

    def remove_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        save([t.to_dict() for t in self.tasks])

    def update_task(self, task_id: int, task=None, priority=None, done=None):
        for t in self.tasks:
            if t.id == task_id:
                if task is not None:
                    t.task = task
                if priority is not None:
                    t.priority = priority
                if done is not None:
                    t.done = done

                save([x.to_dict() for x in self.tasks])
                return t

        return None

    def toggle_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            save(self.tasks)

    def search(self, keyword: str):
        keyword = keyword.lower()

        return [
            t for t in self.tasks
            if keyword in t.task.lower()
    ]

