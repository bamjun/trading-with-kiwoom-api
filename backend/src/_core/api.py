from backend.src._core.router import router as core_router
from backend.src.a_stocks._router import stocks as stocks_router
from ninja import NinjaAPI

api = NinjaAPI(
    title="A Stocks API",
    description="API for A Stocks",
    version="0.0.1",
)

api.add_router("/", core_router, tags=["core"])
api.add_router("/stocks", stocks_router, tags=["stocks"])
