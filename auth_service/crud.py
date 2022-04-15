from sqlalchemy.orm import Session
import model, schemas

def get_user(db: Session, user_login: str):
    return db.query(model.User).filter(model.User.login == user_login).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User):
    db_user = model.User(login=user.login, token=user.token, scope=user.scope, token_type=user.token_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, login: str):
    user = db.query(model.User).filter(model.User.login == login).first()
    if user:
        db.delete(user)
        db.commit()
        db.refresh(user)
        return True
    else:
        return False
