from importlib import import_module
from pathlib import Path

from fastapi import APIRouter

from de_demo import apps

api_router = APIRouter()

root = apps.__path__[0]

routers = Path(root).glob("*/api/router.py")

for submodule_path in routers:
    submodule = str(submodule_path.absolute())[len(root)+1:-3]
    submodule = submodule.replace("/", ".")

    module = import_module(f"{apps.__name__}.{submodule}")
    for obj in vars(module).values():
        if isinstance(obj, APIRouter):
            api_router.include_router(obj)
