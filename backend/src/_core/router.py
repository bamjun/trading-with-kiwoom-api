from django.http import HttpRequest
from ninja.router import Router

router = Router()


@router.get("/health")
def health_check(request: HttpRequest) -> dict[str, str]:
    """
    Health check endpoint
    """
    return {"status": "ok"}
