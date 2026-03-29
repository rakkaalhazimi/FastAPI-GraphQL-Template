import sqlite3
from typing import Optional, Tuple

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import strawberry
from strawberry.fastapi import BaseContext

from app.user.user_types import UserPayload



class GraphQLContext(BaseContext):
    def __init__(
            self, 
            db: sqlite3.Connection,
            user: Tuple[UserPayload, HTTPException],
            db_session: Session,
        ):
        self.db = db
        self.user = user
        self.db_session = db_session

GraphQLInfo = strawberry.Info[GraphQLContext, None]