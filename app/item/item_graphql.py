from typing import List, Optional

import strawberry

from app.auth.auth_service import IsAuthenticated
from app.context import GraphQLInfo

from app.item.item_service import item_service
from app.item.types import ItemQL



@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def all_items(self, info: GraphQLInfo) -> List[ItemQL]:
        db_session = info.context.db_session
        user_payload, _ = info.context.user
        items = item_service.get_all_items(db_session, user_payload.id)
        return items


    @strawberry.field
    def item_by_id(
            self, 
            info: GraphQLInfo,
            id: strawberry.ID
    ) -> Optional[ItemQL]:
        db_session = info.context.db_session
        user_payload, _ = info.context.user
        item = item_service.get_item_by_id(db_session, user_payload.id, id)
        return item
        

@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_item(
            self, 
            info: GraphQLInfo,
            name: str, 
            description: Optional[str] = None
    ) -> ItemQL:
        db_session = info.context.db_session
        user_payload, _ = info.context.user
        item = item_service.create_item(
            db_session, 
            user_payload.id, 
            name, 
            description
        )
        return item

    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_item_name(
            self,
            info: GraphQLInfo,
            id: strawberry.ID, 
            name: str, 
    ) -> Optional[ItemQL]:
        db_session = info.context.db_session
        user_payload, _ = info.context.user
        item = item_service.update_item_name(db_session, user_payload.id, id, name)
        return item
    
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_item_description(
            self,
            info: GraphQLInfo,
            id: strawberry.ID, 
            description: str, 
    ) -> Optional[ItemQL]:
        db_session = info.context.db_session
        user_payload, _ = info.context.user
        item = item_service.update_item_description(db_session, user_payload.id, id, description)
        return item


    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_item(
            self, 
            info: GraphQLInfo, 
            id: strawberry.ID
    ) -> bool:
        db_session = info.context.db_session
        user_payload, _ = info.context.user
        item = item_service.delete_item(db_session, user_payload.id, id)
        return item
        