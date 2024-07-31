"""
api.py
---

The REST Api.
"""

from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def welcome():
    date = datetime.now()
    return {"message": f"Welcome to the API at {date}"}
