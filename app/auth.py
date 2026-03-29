from typing import Optional, Tuple, List
from datetime import datetime, timedelta, timezone
from dataclasses import asdict
import re

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash
from strawberry.exceptions import StrawberryGraphQLError
from strawberry.permission import BasePermission

from app.context import GraphQLInfo
from app.settings import settings

from app.user.user_types import UserPayload



# API Key
api_key_header = APIKeyHeader(name="api-key")

def api_key_auth(api_key: str = Depends(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



# User Login and Registration
password_hash = PasswordHash.recommended()

def get_password_hash(password: str):
    return password_hash.hash(password)

def verify_user_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def check_email(email: str):
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    return re.fullmatch(regex, email)

def check_username(username: str):
    special_symbols = ["_"]
    val = True
    error_messages = []

    if len(username) < 4:
        error_messages.append("Username should be at least 4 characters")
        val = False
    if len(username) > 20:
        error_messages.append("Username should not be greater than 20 characters")
        val = False
        
    for char in username:
        if 48 <= ord(char) <= 57:
            pass
        elif 65 <= ord(char) <= 90:
            pass
        elif 97 <= ord(char) <= 122:
            pass
        elif char in special_symbols:
            pass
        else:
            error_messages.append(
                f"Username '{username}' should only contain numbers" +
                f", lowercase and uppercase letters, and {special_symbols}"
            )
            val = False
    
    return val, error_messages

def check_password(password: str) -> Tuple[bool, List[str]]:
    special_symbols = ["$", "@", "#", "%", "!", "*"]
    val = True
    error_messages = []

    if len(password) < 8:
        error_messages.append("Password should be at least 8 characters")
        val = False
    if len(password) > 20:
        error_messages.append("Password should not be greater than 20 characters")
        val = False

    has_digit = has_upper = has_lower = has_sym = False

    for char in password:
        if 48 <= ord(char) <= 57:
            has_digit = True
        elif 65 <= ord(char) <= 90:
            has_upper = True
        elif 97 <= ord(char) <= 122:
            has_lower = True
        elif char in special_symbols:
            has_sym = True

    if not has_digit:
        error_messages.append("Password should have at least one numeral")
        val = False
    if not has_upper:
        error_messages.append("Password should have at least one uppercase letter")
        val = False
    if not has_lower:
        error_messages.append("Password should have at least one lowercase letter")
        val = False
    if not has_sym:
        error_messages.append(
            f"Password should have at least one of the symbols: {special_symbols}")
        val = False
    
    print(error_messages)

    return val, error_messages



# JWT
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def create_access_token(
        data: UserPayload, 
        expires_delta: timedelta | None = None
) -> str:
    to_encode = asdict(data)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        token: Optional[str] = Depends(oauth2_scheme)
) -> Tuple[UserPayload, Exception]:
    try:
        if not token:
            return None, HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        jwt_decoded = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_payload = UserPayload.from_dict(jwt_decoded)
        return user_payload, None
    
    except jwt.ExpiredSignatureError:
        # print("Error: The token has expired.")
        return None, HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The token has expired"
        )

    except jwt.InvalidTokenError as e:
        # print(f"Error: Invalid token - {e}")
        return None, HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None, HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Strawberry Permission
class IsAuthenticated(BasePermission):
    def has_permission(self, source, info: GraphQLInfo, **kwargs) -> bool:
        user, error = info.context.user
        if error:
            raise StrawberryGraphQLError(
                message=error.detail,
                extensions={
                    "status_code": error.status_code,
                    "type": "AUTHENTICATION_ERROR",
                },
                original_error=error
            )
        if user:
            return True
        return False