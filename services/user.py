import random
import string
from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from exceptions import UsernameAlreadyUsedException
from repository.user import UserRepository
from schemas import UserLoginSchema
from services.auth import AuthService


@dataclass
class UserService:
    user_repository:  UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        try:
            user = self.user_repository.create_user(
                username=username,
                password=password,
            )
        except IntegrityError:
            raise UsernameAlreadyUsedException

        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(
            user_id=user.id,
            access_token=access_token
        )

