from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.middlewares import process_time_middleware
from src.api.routers import health_router, login_router, transcribe_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(process_time_middleware.ProcessTimeMiddleware)
    app.include_router(health_router.router)
    app.include_router(login_router.router)
    app.include_router(transcribe_router.router)
    return app


load_dotenv()

app = create_app()
