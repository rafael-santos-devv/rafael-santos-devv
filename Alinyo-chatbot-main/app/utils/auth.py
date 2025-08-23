from fastapi import Depends, Header, HTTPException
from sqlmodel import Session
from app.database import engine, get_session
from app.models import User

def get_current_user(session: Session = Depends(get_session), user_id: int = Header(...)):
    with session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        return user
