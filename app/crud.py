from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.user import User # Solo necesitamos el modelo de la BD

def get_user_by_username(session: Session, username: str) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()

# La función ahora recibe un objeto User ya listo para la BD
def create_user(session: Session, user: User) -> User:
    # Las validaciones de duplicados se quedan aquí, ya que son una operación de BD
    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de usuario ya existe.")
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado.")

    # Simplemente añade el objeto a la sesión y lo guarda
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user