import strawberry

from app.auth import IsAuthenticated
from app.context import GraphQLInfo

from app.user.user_types import UserQL
from app.user.user_service import user_service



@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_user_by_id(self, info: GraphQLInfo, id: strawberry.ID) -> UserQL:
        user = user_service.getUserById(id)
        if user:
            user_ql = user_service.create_user_ql(user)
            return user_ql
        return None


@strawberry.type
class Mutation:
    @strawberry.field()
    def login(
        self, 
        info: GraphQLInfo, 
        username_or_email: str, 
        password: str
    ) -> str:
        db_session = info.context.db_session
        access_token = user_service.login_user(db_session, username_or_email, password)
        return access_token
    
    
    @strawberry.field()
    def register_user(
            self,
            info: GraphQLInfo,
            username_or_email: str,
            password: str,
    ) -> UserQL:
        db_session = info.context.db_session
        user = user_service.register_user(db_session, username_or_email, password)
        return user