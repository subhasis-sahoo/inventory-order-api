from fastapi import FastAPI

from app.routers.product_router import router as product_router
from app.routers.user_router import router as user_router
from app.routers.order_router import router as order_router

# from app.database.connection import engine, Base
# from app.database import models


# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory & Order Management API")


@app.get("/")
def root():
    return {"message": "Inventory API is running"}

app.include_router(product_router)
app.include_router(user_router)
app.include_router(order_router)
