from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from core.config import settings
from models.auth import NewToken, Token
from models.response import Response

from components.authentication.auth_manager import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
)


async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Response[NewToken]:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})
    return Response(
        status="OK",
        data=NewToken(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        ),
    )


async def refresh_token(refresh_token: str) -> Response[Token]:
    try:
        payload = (
            jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            ),
        )
        username = payload[0].get("sub", None)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Response(
        status="OK", data=Token(access_token=new_access_token, token_type="Bearer")
    )
