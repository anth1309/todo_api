
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from service import ToDoService

app = FastAPI()
service = ToDoService()

class TaskIn(BaseModel):
    task: str
    priority: int

class TaskUpdate(BaseModel):
    task: str = None
    priority: int = None
    done: bool = None

@app.get("/tasks")
def get_tasks(
    done: bool = None,
    priority: int = None,
    page: int = 1,
    limit: int = 10,
    sort: str = "priority"
):
    return service.get_tasks(done, priority, page, limit, sort)

@app.post("/tasks")
def add_task(data: TaskIn):
    service.add_task(data.task, data.priority)
    return {"message": "task added"}

@app.get("/tasks/search")
def search_tasks(keyword: str = ""):
    return service.search(keyword)

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in service.tasks:
        if task.id == task_id:
            return task.to_dict()
    return {"error": "Task not found"}

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    service.remove_task(task_id)
    return {"message": "task removed"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    updated = service.update_task(
        task_id,
        data.task,
        data.priority,
        data.done
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated.to_dict()


