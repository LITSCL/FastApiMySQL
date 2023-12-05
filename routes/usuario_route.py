from fastapi import APIRouter
from typing import List

from config.database import DataBase
from models.usuario import Usuario, tabla_usuario
from schemas.usuario_schema import objeto_schema, lista_schema

db: object = DataBase().get_conexion()
router: object = APIRouter()

query: object = None

@router.post("/usuario/save", response_model = int, tags = ["modelo_usuario"])
async def save_usuario(usuario: Usuario) -> int:
    usuario_obtenido: dict = dict(usuario)
    usuario_obtenido.pop("id")
    query = db.execute((tabla_usuario).insert().values(usuario_obtenido))
    db.commit()
    resultado: int = query.inserted_primary_key[0]
    return resultado

@router.get("/usuario", response_model = List[Usuario], tags = ["modelo_usuario"])
async def get_usuarios() -> list:
    query = db.execute((tabla_usuario).select()).fetchall()
    resultado: list = lista_schema(query)
    return resultado

@router.get("/usuario/{key}", response_model = Usuario, tags = ["modelo_usuario"])
async def get_usuario(key: int) -> dict:
    query = db.execute((tabla_usuario).select().where(key == tabla_usuario.c.id)).first()
    resultado: dict = objeto_schema(query)
    return resultado

@router.put("/usuario/{key}", response_model = Usuario, tags = ["modelo_usuario"])
async def update_usuario(key: int, usuario: Usuario) -> dict:
    usuario_obtenido: dict = objeto_schema(usuario)
    query = db.execute((tabla_usuario).update().values(usuario_obtenido).where(key == tabla_usuario.c.id))
    query = db.execute((tabla_usuario).select().where(key == tabla_usuario.c.id)).first()
    db.commit()
    resultado: dict = objeto_schema(query)
    return resultado

@router.delete("/usuario/{key}", response_model = Usuario, tags = ["modelo_usuario"])
async def delete_usuario(key: int) -> dict:
    query = db.execute((tabla_usuario).select().where(key == tabla_usuario.c.id)).first()
    usuario_obtenido: dict = objeto_schema(query)
    query = db.execute((tabla_usuario).delete().where(key == tabla_usuario.c.id))
    db.commit()
    resultado: dict = usuario_obtenido
    return resultado

rutas_usuario: object = router