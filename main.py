from fastapi import FastAPI

from session import session_controller
from transaction import transaction_controller
from user import user_controller

app = FastAPI()

app.include_router(user_controller.router)
app.include_router(session_controller.router)
app.include_router(transaction_controller.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/")
async def say_hello():
    return {"message": "Hello World"}
