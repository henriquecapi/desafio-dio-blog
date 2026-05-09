import time
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Annotated

SECRET = "my-super-secret-key-that-is-at-least-32-characters-long"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: str
    aud: str | list[str]
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"


def sign_jwt(user_id: int) -> dict:
    now = time.time()
    payload = {
        "iss": "http://localhost:8000",
        "sub": str(user_id),
        "aud": "capi-blog",
        "exp": now + 60 * 60,  # 1 hora
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "Bearer"}


async def decode_jwt(token: str) -> AccessToken | None:
    try:
        decoded_payload = jwt.decode(
            token, SECRET, audience="capi-blog", algorithms=[ALGORITHM]
        )
        # jwt.decode já valida exp, iat e nbf — se chegou aqui, o token é válido
        return AccessToken.model_validate(decoded_payload)
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessToken:
        authorization: str = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Scheme de autenticação inválido!",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            payload = await decode_jwt(credentials)

            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido ou expirado!",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return payload
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autorização de Bearer inválida",
                headers={"WWW-Authenticate": "Bearer"},
            )


async def get_current_user(
    token: Annotated[AccessToken, Depends(JWTBearer())],
) -> dict[str, int]:
    return {"user_id": int(token.sub)}


def login_required(
    current_user: Annotated[dict[str, int], Depends(get_current_user)],
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
