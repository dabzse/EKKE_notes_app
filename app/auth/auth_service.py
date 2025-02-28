from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.crud import get_user
from app.models import User

"""
to get a SECRET_KEY string, run:
openssl rand -hex 32
"""
SECRET_KEY = "222adc0c77257f628b56c5502b6b2e2b5018d95cb7efbc1ebb50657f26faac49"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(payload: dict):
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dictionary")
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get('sub')
        if not sub:
            raise ValueError("Invalid 'sub' field in token payload")
        return payload
    except (JWTError, ValueError) as e:
        print(f"Error decoding token: {e}")
        return None
