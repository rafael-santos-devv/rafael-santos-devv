from fastapi import APIRouter, HTTPException, Header, Depends
from sqlmodel import Session
from app.models import User, UserCreate, UserLogin
from app.database import engine, get_session
from app.utils.security import hash_password, verify_password

router = APIRouter()

@router.post("/cadastro")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
        existing_user = session.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        new_user = User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password)
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"mensagem": "Usuário criado com sucesso", "usuario_id": new_user.id}
    
@router.post("/login")
def login_user(data: UserLogin, session: Session = Depends(get_session)):
    user_from_db = session.query(User).filter(User.email == data.email).first()

    if not user_from_db:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

    if not verify_password(data.password, user_from_db.password):
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    return {
        "message": "Login bem-sucedido",
        "user_id": user_from_db.id,
        "name": user_from_db.name
    }

