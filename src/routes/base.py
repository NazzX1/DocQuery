from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import Settings,  get_settings


base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/welcome")
async def welcome(app_settings : Settings = Depends(get_settings)):

    # app_settings = get_settings()

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION


    return {
        "message" : f'Hello from {app_name}',
        "version" : f'{app_version}'

    }