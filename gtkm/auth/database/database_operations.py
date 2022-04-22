from sqlalchemy.orm import Session
from .user_model import UserModel
from .user_schema import User


def get_user(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_github_login(db: Session, login: str):
    return db.query(UserModel).filter(UserModel.github_login == login).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: User):
    db_user = UserModel(id=user.id, github_login=user.github_login, github_token=user.github_token,
        gitlab_login=user.gitlab_login, gitlab_token=user.gitlab_token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        db.refresh(user)
        return True
    else:
        return False