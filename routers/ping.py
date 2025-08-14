from fastapi import APIRouter
from fastapi.params import Depends

from dependency import get_request_user_id

router = APIRouter(
    prefix="/ping",
    tags=['Ping'],
)

@router.get("")
def get_ping(user_id: int = Depends(get_request_user_id)):
    return {"message": "Pong!"}