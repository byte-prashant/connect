import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from app.api.v1.recipe import app_router
from app.config import settings
from fastapi_versioning import VersionedFastAPI, version
app = FastAPI(title="Connect")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter(prefix="/api")
api_router.include_router(app_router)
app.include_router(api_router)
# app = VersionedFastAPI(app)
