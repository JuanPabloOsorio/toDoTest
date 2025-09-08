from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.api.routes import (
    task,
    lists
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],      # Permite todos los métodos (GET, POST, PUT, DELETE...)
    allow_headers=["*"],      # Permite todas las cabeceras
)

app.include_router(task.router)
app.include_router(lists.router)
