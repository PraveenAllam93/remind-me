from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from config.openai_client import openai_client
from config.settings import settings
from logs import setup_logging

setup_logging()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="NA",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    contact={"name": "Praveen Allam", "email": "saipraveen.allam@copart.com"},
    debug=settings.DEBUG,
)
app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health Check"])
def health_check() -> dict:
    health_data = {"status": "healthy"}
    return health_data


# for router_module in router_modules:
#     app.include_router(router_module.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)
