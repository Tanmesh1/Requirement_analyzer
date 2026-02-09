from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# Configure password hashing
pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    bycrypt supports max 72 bytes.
    """
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password to long (max 72 characters).")
    return pwd_context.hash(password)


def verify_password(plain_password:str , hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hash.
    """
    return pwd_context.verify(plain_password,hashed_password)

#-----------------
# JWT CONFIGURATION
#-----------------

SECRET_KEY = "CHANGE_THIS_SECRET_IN_PROD"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str) -> dict:
    """
    Decode and validate a JWT token.
    Returns payload if valid.
    Raise exception if invalid.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise ValueError("Invalid or Expired Token")