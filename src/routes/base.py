from fastapi import FastAPI, APIRouter, Depends, Request, status
import os

from fastapi.responses import JSONResponse
from helpers.config import Settings,  get_settings
from models.enums.ResponseEnums import ResponseSignal

from .schemes.user import LoginRequest, RegisterRequest
from models.UserModel import UserModel
from models.db_schemes import User


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


@base_router.post("/register")
async def register(request : Request ,register_request : RegisterRequest):

    
    user_model = await UserModel.create_instance(
        db_client = request.app.db_client
    )

    user = User(
        username = register_request.username,
        email = register_request.email,
        password = register_request.password
    )
    result = await user_model.register(user = user)

    if not result:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal" :  ResponseSignal.USER_REGISTER_ERROR.value ,
            }
        )
    
    return JSONResponse(
            content={
                "signal" :  ResponseSignal.USER_REGISTER_SUCCESS.value 
            }
        )


@base_router.post("/login")
async def login(request : Request ,login_request : LoginRequest):

    
    user_model = await UserModel.create_instance(
        db_client = request.app.db_client
    )

    result = await user_model.login(
        email = login_request.email,
        password = login_request.password
    )

    if not result:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal" :  ResponseSignal.USER_LOGIN_ERROR.value ,
            }
        )
    
    return JSONResponse(
            content={
                "signal" :  ResponseSignal.USER_LOGIN_SUCCESS.value 
            }
        )
