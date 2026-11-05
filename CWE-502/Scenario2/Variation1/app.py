from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-change-me"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass
class Task:
    title: str
    priority: Priority = Priority.MEDIUM
    due: date | None = None
    tags: set[str] = field(default_factory=set)
    done: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Workspace:
    name: str
    owner: str
    tasks: dict[str, Task] = field(default_factory=dict)

    def add(self, task:Task) -> Task:
        self.tasks[task.id] = task
        return task

workspace = Workspace(name="Team board", owner="Alice")
workspace.add(Task("Write onboarding doc", Priority.HIGH, date(2026, 12, 1), {"docs"}))
workspace.add(Task("Fix login redirect", Priority.MEDIUM, None, {"bug", "auth"}))
workspace.add(Task("Plan Q1 offsite", Priority.LOW, date(2027, 1, 15),{"team"}))

@app.route("/")
def index():
    tasks = sorted(
        workspace.tasks.values(),
        key=lambda t: (t.done, -t.priority.value, t.created_at),
    )
    return render_template(
        "index.html",workspace=workspace, tasks=tasks, priorities=list(Priority)
    )

@app.post("/tasks")
def add_task():
    title = request.form.get("title","").strip()
    if not title or len(title) > 200:
        abort(400)
    
    try:
        priority = Priority[request.form.get("priority","MEDIUM")]
    except KeyError:
        abort(400)
    tags = {t.strip().lower() for t in request.form.get("tags","").split(",") if t.strip()}

    workspace.add(Task(title=title, priority=priority, due=due, tags=tags))
    return redirect(url_for("index"))

@app.post("/tasks/<task_id>/toggle")
def toggle_task(task_id: str):
    task = workspace.tasks.get(task_id)
    if task is None:
        abort(404)
    task.done = not task.done
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)