from fastapi import FastAPI

from src.api.routes import index_price

app = FastAPI()
app.include_router(index_price.router)
