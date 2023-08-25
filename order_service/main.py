from fastapi import FastAPI
from .api import router as order_router

app = FastAPI()

app.include_router(order_router, prefix="/orders", tags=["order_service"])