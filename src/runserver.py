import os
import threading

from dotenv import load_dotenv

from adapters.grpc.grpc_server import start_grpc_server
from adapters.rest.rest_server import start_rest_server
from core.container import Container


def main() -> None:
    load_dotenv()

    host = os.getenv("HOST", "127.0.0.1")
    rest_port = os.getenv("REST_PORT", "8000")
    grpc_port = os.getenv("GRPC_PORT", "8001")

    container = Container()

    grpc_thread = threading.Thread(target=start_grpc_server, args=(host, grpc_port))
    rest_thread = threading.Thread(target=start_rest_server, args=(host, rest_port, container))

    grpc_thread.start()
    rest_thread.start()

    grpc_thread.join()
    rest_thread.join()


if __name__ == "__main__":
    main()
