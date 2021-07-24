from fastapi import APIRouter, Response, status
from starlette.status import HTTP_204_NO_CONTENT
from config.db import conn
from models.user import users
from schemas.user import User

from cryptography.fernet import Fernet

# En la variable key se genera un numero random para hacer unico cada uno de los cifrados
key = Fernet.generate_key()

# f es a funcion para cifrar
f = Fernet(key)

user = APIRouter()


@user.get('/users', response_model=list, tags=["Users"])
def get_users():
    # Se retornan los usuarios consultados de la base de datos
    return conn.execute(users.select()).fetchall()


@user.post('/users', response_model=User,tags=["Users"])
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    # Encriptación de la contraseña
    new_user["password"] = f.encrypt((user.password.encode("utf-8")))
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get('/users/{id}', response_model=User,tags=["Users"])
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete('/users/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Users"])
def delete_user(id: str):
    result = conn.execute(users.delete().where(user.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put('/users/{id}', response_model=User,tags=["Users"])
def update_user(id: str, user: User):
    conn.execute(users.update().values(name=user.name, email=user.email, password=f.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()
