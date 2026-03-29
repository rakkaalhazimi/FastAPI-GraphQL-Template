from typing import Sequence, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from app.item.model import Item



class ItemRepository:
    def get_all_items(self, session: Session, user_id: int) -> Sequence[Item]:
        query = select(Item).where(Item.user_id == user_id)
        result = session.execute(query)
        return result.scalars().all()


    def get_item_by_id(self, session: Session, item_id: int) -> Optional[Item]:
        query = select(Item).where(Item.id == item_id)
        result = session.execute(query)
        return result.scalar_one_or_none()
    
    
    def get_item_by_id_and_user(self, session: Session, user_id: int, item_id: int):
        query = select(Item).where(Item.id == item_id, Item.user_id == user_id)
        return session.execute(query).scalar_one_or_none()


    def create_item(self, session: Session, name: str, user_id: int, description: Optional[str] = None) -> Item:
        new_item = Item(name=name, description=description, user_id=user_id)
        session.add(new_item)
        session.flush()  # Populates the ID without committing the whole transaction
        return new_item


    def update_item_name(self, session: Session, item_id: int, name: str) -> Optional[Item]:
        query = (
            update(Item)
            .where(Item.id == item_id)
            .values(name=name)
            .returning(Item)
        )
        result = session.execute(query)
        return result.scalar_one_or_none()


    def update_item_description(self, session: Session, item_id: int, description: str) -> Optional[Item]:
        query = (
            update(Item)
            .where(Item.id == item_id)
            .values(description=description)
            .returning(Item)
        )
        result = session.execute(query)
        return result.scalar_one_or_none()


    def delete_item(self, session: Session, item_id: int) -> bool:
        query = delete(Item).where(Item.id == item_id).returning(Item.id)
        result = session.execute(query)
        deleted_id = result.scalar_one_or_none()
        return deleted_id is not None


item_repository = ItemRepository()