import os

from dotenv import load_dotenv

from adapters.rest.rest_server import start_rest_server


def main() -> None:
    load_dotenv()

    host = os.getenv("HOST", "127.0.0.1")
    rest_port = os.getenv("REST_PORT", "8000")

    start_rest_server(host=host, port=rest_port)


if __name__ == "__main__":
    main()
