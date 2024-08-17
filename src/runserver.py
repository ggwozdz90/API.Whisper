import os

import uvicorn


def main() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run(
        "api.fast_api:app",
        host=host,
        port=8000,
        reload=True,
        server_header=False,
    )


if __name__ == "__main__":
    main()
