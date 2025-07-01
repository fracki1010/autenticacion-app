from sqlmodel import SQLModel, Field
from typing import Optional

# Esquema para devolver datos seguros del usuario al cliente
class UserPublic(SQLModel):
    id: int
    username: str
    full_name: str
    email: str
    disabled: bool

# Esquema para recibir los datos al crear un usuario
class UserCreate(SQLModel):
    username: str
    full_name: str
    email: str
    password: str # Se recibe la contraseña en texto plano

# Modelo de la tabla de base de datos
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: str
    email: str = Field(unique=True)
    hashed_password: str
    disabled: bool = False