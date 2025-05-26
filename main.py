from fastapi import APIRouter, FastAPI
from fastapi.security  import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware


#local files
from core.database import engine
from auth.routers.auth import auth_router
from user.routers.user import user_router

# from core.config_loader import settings

app = FastAPI()

# if settings.BACKEND_CORS_ORIGINS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes

app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(user_router, prefix="/api", tags=["user"])

@app.get("/")
async def root():
    return {"message": "Hello World"}




# models.Base.metadata.create_all(bind= engine)