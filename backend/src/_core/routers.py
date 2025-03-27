from ninja.router import Router

from django.http import HttpRequest

router = Router()


@router.get("/health")
def health_check(request: HttpRequest) -> dict[str, str]:
    """
    Health check endpoint
    """
    return {"status": "ok"}
