import bcrypt
import joserfc as jwt
from models.users import BaseUser
from core.settings import settings
from datetime import datetime, timezone, timedelta
from core.exceptions import TokenCreationException,TokenValidationException,TokenExpiredException

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(user: BaseUser):
    try:
        claims = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        header = {
            "alg":settings.ALG,
        }

        secret = jwt.jwk.import_key(settings.SECRET, "oct")
        token = jwt.encode(header,claims, secret)
        return token
    except Exception as e:
        raise TokenCreationException(str(e))
        
def create_refresh_token(user: BaseUser):
    try:
        claims = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(days=7)
        }

        header = {
            "alg":settings.ALG,
        }

        secret = jwt.jwk.import_key(settings.SECRET, "oct")
        token = jwt.encode(header,claims, secret)
        return token
    except Exception as e:
        raise TokenCreationException(str(e))

def decode_token(token:str):
    try:
        header, claims = jwt.decode(token, jwt.jwk.import_key(settings.SECRET, "oct"))

        if claims["exp"] < datetime.now(timezone.utc):
            raise TokenExpiredException()

        return claims
    except jwt.exceptions.InvalidClaimError as e:
        raise TokenValidationException(str(e))
    except Exception as e:
        raise TokenValidationException(str(e))