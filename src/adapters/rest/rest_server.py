import uvicorn
from fastapi import FastAPI

from src.adapters.rest.middlewares import process_time_middleware
from src.adapters.rest.routers import health_router, login_router, transcribe_router


def start_rest_server(
    host: str,
    port: str,
) -> None:
    config = uvicorn.Config(
        "src.adapters.rest.rest_server:app",
        host=host,
        port=int(port),
        reload=True,
        server_header=False,
    )
    server = uvicorn.Server(config)
    server.run()


def _create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(process_time_middleware.ProcessTimeMiddleware)
    app.include_router(health_router.router)
    app.include_router(login_router.router)
    app.include_router(transcribe_router.router)
    return app


app = _create_app()
