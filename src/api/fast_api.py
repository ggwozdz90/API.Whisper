from dotenv import load_dotenv
from fastapi import FastAPI

from .middlewares import process_time_middleware
from .routers import auth_router, health_router, transcribe_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(process_time_middleware.ProcessTimeMiddleware)
    app.include_router(health_router.router)
    app.include_router(auth_router.router)
    app.include_router(transcribe_router.router)
    return app


load_dotenv()

app = create_app()
