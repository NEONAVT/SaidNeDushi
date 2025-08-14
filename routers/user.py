from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from dependency import get_user_service
from exceptions import UsernameAlreadyUsedException
from schemas import UserLoginSchema, UserCreateSchema
from services import UserService

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("", response_model=UserLoginSchema)
def create_user(
        body: UserCreateSchema,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        return user_service.create_user(body.username, body.password)
    except UsernameAlreadyUsedException as e:
        raise HTTPException(status_code=400, detail=e.detail)