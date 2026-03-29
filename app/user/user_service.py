from fastapi import status
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    check_username, 
    check_email, 
    check_password,
    get_password_hash,
    verify_user_password,
)
from app.response import create_strawberry_response_error

from app.user.model import User
from app.user.repository.user_repository import user_repository
from app.user.user_types import UserPayload, UserQL



class UserService:
    def create_user_ql(self, user: User) -> UserQL:
        return UserQL(
            id=user.id, 
            username=user.username, 
            email=user.email
        )
    
    
    def login_user(self, session: Session, username_or_email: str, password: str) -> str:
        found_user = user_repository.get_user_by_username_or_email(session, username_or_email)
        if not found_user:
            error = ValueError(f"Username or Email, {username_or_email} hasn't been registered")
            raise create_strawberry_response_error(error, status.HTTP_401_UNAUTHORIZED)
        
        hashed_password = found_user.password
        is_valid = verify_user_password(password, hashed_password)
        if not is_valid:
            error = ValueError("Username, Email or Password are incorrect")
            raise create_strawberry_response_error(error, status.HTTP_401_UNAUTHORIZED)
        
        user_payload = UserPayload(
            id=found_user.id, 
            username=found_user.username, 
            email=found_user.email
        )
        access_token = create_access_token(user_payload)
        
        return access_token
    

    def register_user_by_username(self, session: Session, username: str, password: str) -> User:
        is_user_valid, user_errors = check_username(username)
        if not is_user_valid:
            error = ValueError("\n".join(user_errors))
            raise create_strawberry_response_error(error, status.HTTP_400_BAD_REQUEST)
        
        hashed_pwd = get_password_hash(password)

        found_user = user_repository.get_user_by_username_or_email(session, username)
        if found_user:
            error = ValueError(f"Username '{username}' has already been used")
            raise create_strawberry_response_error(error, status.HTTP_409_CONFLICT)
        
        new_user = user_repository.create_user_by_username(session, username, hashed_pwd)
        return new_user
        
        
    def register_user_by_email(self, session: Session, email: str, password: str) -> User:
        is_email_valid = check_email(email)
        if not is_email_valid:
            error = ValueError(f"'{email}' is not a valid email format")
            raise create_strawberry_response_error(error, status.HTTP_400_BAD_REQUEST)

        hashed_pwd = get_password_hash(password)
        
        found_user = user_repository.get_user_by_username_or_email(session, email)
        if found_user:
            error = ValueError(f"Email '{email}' has already been used")
            raise create_strawberry_response_error(error, status.HTTP_409_CONFLICT)
        
        new_user = user_repository.create_user_by_email(session, email, hashed_pwd)
        return new_user


    def register_user(self, session: Session, username_or_email: str, password: str) -> UserQL:
        is_pwd_valid, pwd_errors = check_password(password)
        if not is_pwd_valid:
            error = ValueError("\n".join(pwd_errors))
            raise create_strawberry_response_error(error, status.HTTP_400_BAD_REQUEST)
        
        if "@" in username_or_email:
            new_user = user_service.register_user_by_email(session, username_or_email, password)
        else:
            new_user = user_service.register_user_by_username(session, username_or_email, password)

        try:
            session.commit()
            session.refresh(new_user)
            return self.create_user_ql(new_user)
        except Exception as e:
            session.rollback()
            raise e


    def get_user(self, session: Session, user_id: int) -> UserQL:
        user = user_repository.get_user_by_id(session, user_id)
        if not user:
            return None
        return self.create_user_ql(user)


user_service = UserService()