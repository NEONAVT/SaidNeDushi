from fastapi import Depends, Request, security, HTTPException
from fastapi.params import Security
from sqlalchemy.orm import Session

from cache import get_redis_connection
from database import get_db_session
from exceptions import TokenExpired, TokenNotValid
from repository import UserRepository, TaskCache
from repository.tasks import TaskRepository, CategoryRepository
from services.auth import AuthService
from services.tasks import TasksService, CategoryService
from services.user import UserService



def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session=db_session)


def get_category_repository(db_session: Session = Depends(get_db_session)) -> CategoryRepository:
    return CategoryRepository(db_session=db_session)

def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_tasks_service(
        tasks_repository: TaskRepository = Depends(get_tasks_repository),
        tasks_cache: TaskCache = Depends(get_tasks_cache_repository)
) -> TasksService:
    return TasksService(tasks_repository=tasks_repository, tasks_cache=tasks_cache)


def get_category_service(
        category_repository: CategoryRepository = Depends(get_category_repository)
) -> CategoryService:
    return CategoryService(category_repository=category_repository)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)

reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
        auth_service: AuthService = Depends(get_auth_service)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenNotValid as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_id
