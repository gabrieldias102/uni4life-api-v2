from fastapi import FastAPI
from app.routes import router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API da Uni4Life para rede social de usuários, publicações, comentários, repostagens e conexões.",
)

app.include_router(router, prefix=settings.api_prefix)
