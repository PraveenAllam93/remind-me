from fastapi import APIRouter

from api.api_v1.routers import router_modules

api_router = APIRouter()

for module in router_modules:
    if hasattr(module, "router"):
        api_router.include_router(module.router)
