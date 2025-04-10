from .routes import add_routes

app = None
try:
    from fastapi import APIRouter, FastAPI

    app = FastAPI(title="de-demo")

    api_router = APIRouter()
    add_routes(api_router)

    app.include_router(api_router)
except ImportError:
    pass
