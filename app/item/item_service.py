from typing import List, Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.response import create_strawberry_response_error

from app.item.model import Item
from app.item.repository import item_repository
from app.item.types import ItemQL



class ItemService:
    def create_item_ql(self, item: Item):
        return ItemQL(
            id=item.id, 
            name=item.name, 
            description=item.description
        )
    
    
    def get_all_items(self, session: Session, user_id: int) -> List[ItemQL]:
        items = item_repository.get_all_items(session, user_id)
        return [self.create_item_ql(item) for item in items]


    def get_item_by_id(self, session: Session, user_id: int, item_id: int) -> Optional[ItemQL]:
        item = item_repository.get_item_by_id_and_user(session, user_id, item_id)
        if not item:
            status_code = status.HTTP_404_NOT_FOUND
            error = HTTPException(status_code)
            raise create_strawberry_response_error(error, status_code)
        return self.create_item_ql(item)


    def create_item(
            self, 
            session: Session, 
            user_id: int, 
            name: str, 
            description: Optional[str] = None
    ) -> ItemQL:
        try:
            item = item_repository.create_item(session, name, user_id, description)
            session.commit()
            session.refresh(item)
            return self.create_item_ql(item)
        except Exception as e:
            session.rollback()
            raise e
    
    
    def update_item_name(self, session: Session, user_id: int, item_id: int, name: str) -> Optional[ItemQL]:
        try:
            item = item_repository.get_item_by_id_and_user(session, user_id, item_id)
            if not item:
                status_code = status.HTTP_404_NOT_FOUND
                error = HTTPException(status_code)
                raise create_strawberry_response_error(error, status_code)
            
            item = item_repository.update_item_name(session, item_id, name)
            if item:
                session.commit()
                return self.create_item_ql(item)
            return None
        except Exception as e:
            session.rollback()
            raise e
        

    def update_item_description(self, session: Session, user_id: int, item_id: int, description: str) -> Optional[ItemQL]:
        try:
            item = item_repository.get_item_by_id_and_user(session, user_id, item_id)
            if not item:
                status_code = status.HTTP_404_NOT_FOUND
                error = HTTPException(status_code)
                raise create_strawberry_response_error(error, status_code)
            
            item = item_repository.update_item_description(session, item_id, description)
            if item:
                session.commit()
                return self.create_item_ql(item)
            return None
        except Exception as e:
            session.rollback()
            raise e


    def delete_item(self, session: Session, user_id: int, item_id: int) -> bool:
        try:
            item = item_repository.get_item_by_id_and_user(session, user_id, item_id)
            if not item:
                status_code = status.HTTP_404_NOT_FOUND
                error = HTTPException(status_code)
                raise create_strawberry_response_error(error, status_code)
            
            success = item_repository.delete_item(session, item_id)
            if success:
                session.commit()
            return success
        except Exception as e:
            session.rollback()
            raise e
    

item_service = ItemService()