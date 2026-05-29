from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- IMPORTE O MIDDLEWARE

from app.config import get_settings
from app.database import init_db
from app.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(router, prefix=settings.api_prefix)