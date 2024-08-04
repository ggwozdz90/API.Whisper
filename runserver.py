import uvicorn


def main():
    uvicorn.run(
        "src.api.fast_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        server_header=False,
    )


if __name__ == "__main__":
    main()
