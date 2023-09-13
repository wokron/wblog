from typing import Any
import jwt
from ..dependencies.config import get_settings


def jwt_encode(data: dict[str, Any]):
    setting = get_settings()
    encoded_jwt = jwt.encode(data, key=setting.secret_key, algorithm=setting.algorithm)
    return encoded_jwt


def jwt_decode(encoded_jwt: str):
    setting = get_settings()
    try:
        data = jwt.decode(
            encoded_jwt, key=setting.secret_key, algorithms=setting.algorithm
        )
    except jwt.DecodeError as e:
        return None
    return data
