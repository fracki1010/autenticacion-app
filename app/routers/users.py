from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from app.database import SessionDep
from app.models.user import User, UserCreate, UserPublic
from app.crud import create_user
from app.auth import get_password_hash, authenticate_user, create_access_token, get_current_active_user

router = APIRouter()

@router.post("/users/", response_model=UserPublic, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_new_user(user_data: UserCreate, session: SessionDep):
    """
    Crea un nuevo usuario en el sistema.
    """
    hashed_password = get_password_hash(user_data.password)
    
    user_to_db = User(
        username=user_data.username,
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    return create_user(session=session, user=user_to_db)


@router.post("/token", tags=["Auth"])
def login_for_access_token(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Inicia sesión y devuelve un token de acceso.
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserPublic, tags=["Users"])
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Obtiene los datos del usuario autenticado actualmente.
    """
    return current_user