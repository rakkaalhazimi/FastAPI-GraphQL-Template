from contextlib import asynccontextmanager
from typing import Optional, Tuple

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from app.context import GraphQLContext
from app.db import Base, engine, db_conn, get_db
from app.settings import settings

from app.auth.auth_service import get_current_user
from app.auth.auth_routes import router as auth_router
from app.item import item_graphql
from app.user import user_graphql
from app.user.user_types import UserPayload



# GraphQL
async def get_graphql_context(
        db = Depends(db_conn),
        user: Tuple[UserPayload, Exception] = Depends(get_current_user),
        db_session: Session = Depends(get_db),
) -> GraphQLContext:
    return GraphQLContext(db=db, user=user, db_session=db_session)

Query = merge_types(
    "Query", 
    (
        item_graphql.Query,
        user_graphql.Query,
    )
)
Mutation = merge_types(
    "Mutation", 
    (
        item_graphql.Mutation,
        user_graphql.Mutation,
    )
)
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_graphql_context)


# Fast API App
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up...")
    Base.metadata.create_all(engine)
    yield  # The application starts receiving requests here

    # --- Shutdown Logic (after yield) ---
    print("Application shutting down...")
    print("Resources cleaned up.")


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql", dependencies=[])
app.include_router(auth_router)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)