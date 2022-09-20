from fastapi import APIRouter
from dotenv import load_dotenv
from app.api.v1.routes.profile import jwt_router
from app.api.v1.routes.request_type import requirement_router, requirement_router_v1_1
from app.api.v1.routes.request import help_router
from app.api.v1.routes.assistance import assist_router
from app.api.v1.routes.users import user_router
from fastapi_versioning import VersionedFastAPI, version

load_dotenv('.env')
app_router = APIRouter(prefix="/v1")
app_router.include_router(jwt_router)
app_router.include_router(help_router)
app_router.include_router(requirement_router)
app_router.include_router(assist_router)
app_router.include_router(user_router)