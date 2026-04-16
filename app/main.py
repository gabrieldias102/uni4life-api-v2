from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.database import init_db
from app.routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API da Uni4Life para rede social de usuarios, publicacoes, comentarios, repostagens e conexoes.",
    lifespan=lifespan,
)

app.include_router(router, prefix=settings.api_prefix)
