from sqlalchemy.orm import Session
import model, schemas

def get_user(db: Session, user_id: str):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User):
    db_user = model.User(id=user.id, github_login=user.github_login, github_token=user.github_token,
        gitlab_login=user.gitlab_login, gitlab_token=user.gitlab_token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        db.refresh(user)
        return True
    else:
        return False
