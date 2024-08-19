import os

import uvicorn
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run(
        "src.adapters.rest.fast_api:app",
        host=host,
        port=8000,
        reload=True,
        server_header=False,
    )


if __name__ == "__main__":
    main()
