from dataclasses import dataclass
from jose import jwt, JWTError
from exceptions import UserNotFoundException, IncorrectUserPasswordException, TokenExpired, TokenNotValid
from models import UserProfile
from repository.user import UserRepository
from schemas import UserLoginSchema
import datetime as dt
from datetime import timedelta
from settings import settings

@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise IncorrectUserPasswordException

    @staticmethod
    def generate_access_token(user_id: int) -> str:
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode({
            "user_id": user_id, "expire": expires_date_unix},
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            raise TokenNotValid
        if payload["expire"] < dt.datetime.utcnow().timestamp():
            raise TokenExpired
        return payload["user_id"]


