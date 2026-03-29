from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.user.model import User



class UserRepository:
    def create_user_by_email(self, session: Session, email: str, password: str) -> User:
        new_user = User(email=email, password=password)
        session.add(new_user)
        session.flush() 
        return new_user
        
        
    def create_user_by_username(self, session: Session, username: str, password: str) -> User:
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.flush()
        return new_user
           
            
    def get_user_by_id(self, session: Session, id: int) -> User | None:
        query = select(User).where(User.id == id)
        result = session.execute(query)
        return result.scalar_one_or_none()
    
    
    def get_user_by_username_or_email(self, session: Session, username_or_email: str) -> User | None:
        query = select(User).where(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        )
        result = session.execute(query)
        return result.scalar_one_or_none()


user_repository = UserRepository()