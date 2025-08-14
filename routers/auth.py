
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from typing import Annotated

from dependency import get_auth_service
from exceptions import IncorrectUserPasswordException, UserNotFoundException
from schemas import UserLoginSchema, UserCreateSchema
from services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/login",
    response_model=UserLoginSchema
)
def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return auth_service.login(body.username, body.password)
    except IncorrectUserPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except UserNotFoundException as e:
        raise HTTPException(status_code=401, detail=e.detail)
