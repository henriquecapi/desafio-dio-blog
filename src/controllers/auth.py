from fastapi import APIRouter

from schemas.auth import LoginIn
from security import sign_jwt
from views.auth import LoginOut

auth_router = APIRouter(prefix="/auth")


# checagem -> Buscar usuario na base -> Se existir -> verificar email e a senha -> Criar token -> Retornar token
# se for valida gerar token
@auth_router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    return sign_jwt(user_id=data.user_id)
