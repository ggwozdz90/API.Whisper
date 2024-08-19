from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get(
    "/health",
    tags=["healthcheck"],
    summary="Health Check",
    response_description="Confirm the server is running and healthy.",
    status_code=status.HTTP_200_OK,
)
def health_check() -> Response:
    return Response(status_code=status.HTTP_200_OK)
