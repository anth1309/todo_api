# todo/service.py

import math
from urllib.parse import urlencode

from models import Task
from storage import load, save

ALLOWED_SORTS = ["priority", "task", "done"]


class ToDoService:
    def __init__(self):

        self.tasks = [Task(**t) for t in load()]
        self.next_id = self._get_next_id()
        print("TASKS LOADED:", self.tasks)
    def _get_next_id(self):
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, task, priority):
        new_task = Task(task, priority, id=self.next_id)
        self.next_id += 1
        self.tasks.append(new_task)
        save([t.to_dict() for t in self.tasks])

    def get_tasks(self, done=None, priority=None, page=1, limit=10, sort="priority"):

        filtered = [
            t for t in self.tasks
            if (done is None or t.done == done)
            and (priority is None or t.priority == priority)
        ]

        if sort not in ALLOWED_SORTS:
            sort = "priority"

        if sort == "priority":
            filtered.sort(key=lambda x: x.priority)
        elif sort == "done":
            filtered.sort(key=lambda x: x.done)
        elif sort == "task":
            filtered.sort(key=lambda x: x.task.lower())

        total = len(filtered)
        pages = math.ceil(total / limit) if limit > 0 else 1

        offset = (page - 1) * limit
        paginated = filtered[offset:offset + limit]

        base_params = {
            "done": done,
            "priority": priority,
            "limit": limit,
            "sort": sort
        }

        def build_url(page_num):
            if page_num is None:
                return None
            params = base_params.copy()
            params["page"] = page_num
            return f"/tasks?{urlencode(params)}"

        links = {
            "next": build_url(page + 1 if page < pages else None),
            "prev": build_url(page - 1 if page > 1 else None)
        }

        return {
            "data": [t.to_dict() for t in paginated],
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "pages": pages
            },
            "links": links
        }

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

    def toggle_done(self, task_id: int):
        for t in self.tasks:
            if t.id == task_id:
                t.done = not t.done
                save([x.to_dict() for x in self.tasks])
                return t
        return None

    def search(self, keyword: str):
        keyword = keyword.lower()

        return [
            t for t in self.tasks
            if keyword in t.task.lower()
        ]
