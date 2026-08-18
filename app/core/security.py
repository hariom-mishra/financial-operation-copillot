import bcrypt
from joserfc import jwt
from joserfc import jwk
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

        secret = jwk.import_key(settings.SECRET, "oct")
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

        secret = jwk.import_key(settings.SECRET, "oct")
        token = jwt.encode(header,claims, secret)
        return token
    except Exception as e:
        raise TokenCreationException(str(e))

def decode_token(token: str):
    try:
        secret = jwk.import_key(settings.SECRET, "oct")
        decoded = jwt.decode(token, secret)
        claims = decoded.claims

        exp = claims.get("exp")
        if exp is not None:
            exp_dt = datetime.fromtimestamp(exp, tz=timezone.utc) if isinstance(exp, (int, float)) else exp
            if exp_dt < datetime.now(timezone.utc):
                raise TokenExpiredException()

        return claims
    except TokenExpiredException:
        raise
    except Exception as e:
        raise TokenValidationException(str(e))