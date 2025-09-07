from fastapi import FastAPI
from infrastructure.api.routes import (
    task,
    lists
)

app = FastAPI()

app.include_router(task.router)
app.include_router(lists.router)
