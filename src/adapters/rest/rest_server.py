import uvicorn
from fastapi import FastAPI

from adapters.rest.routers import auth_router, health_router, transcribe_router
from core.container import Container
from src.adapters.rest.middlewares import process_time_middleware


def start_rest_server(
    host: str,
    port: str,
    container: Container,
) -> None:
    container.wire(
        modules=[
            auth_router,
            transcribe_router,
        ]
    )
    config = uvicorn.Config(
        _create_app,
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
    app.include_router(auth_router.router)
    app.include_router(transcribe_router.router)
    return app
