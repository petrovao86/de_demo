from fastapi import FastAPI

from .router import api_router

app = FastAPI(title="de-demo")
app.include_router(api_router)
