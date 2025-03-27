from ninja import NinjaAPI

from _core.routers import router as core_router

api = NinjaAPI(
    title="A Stocks API",
    description="API for A Stocks",
    version="0.0.1",
)

api.add_router("/", core_router, tags=["core"])
