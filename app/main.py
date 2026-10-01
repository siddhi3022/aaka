import logging
import sys
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from .database import Base, engine
from .routes import restaurants, menu, orders

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Food Ordering System",
    version="1.0.0",
    description="Restaurant, menu and order management API with DevOps-ready endpoints.",
)

app.include_router(restaurants.router)
app.include_router(menu.router)
app.include_router(orders.router)

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"service": "food-ordering", "version": app.version, "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
