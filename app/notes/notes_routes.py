from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.auth_service import decode_access_token
from app.crud import (
    create_note as create_note_crud,
    get_notes as get_notes_crud,
    get_note_by_id as get_note_by_id_crud,
    update_note as update_note_crud,
    delete_note as delete_note_crud,
    get_user,
)
from app.models import User
from app.schemas import Note

router = APIRouter()

ERROR_401 = HTTPException(status_code=401, detail="Invalid token")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

templates = Jinja2Templates(directory="app/templates")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"Token received: {token}")
        payload = jwt.decode(
            token,
            "222adc0c77257f628b56c5502b6b2e2b5018d95cb7efbc1ebb50657f26faac49",
            algorithms=["HS256"]
        )
        print(f"Payload decoded: {payload}")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWTError: {e}")
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/notes", response_model=Note)
async def create_note(title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return create_note_crud(db=db, title=title, content=content, owner=owner)


@router.get("/json", response_model=List[Note])  # JSON endpoint
async def get_notes_json(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await get_notes_crud(db, current_user.id)  # Pass user ID


@router.get("/notes", response_class=HTMLResponse)  # HTML endpoint
async def get_notes(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = await get_notes_crud(db, current_user.id)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})


@router.get("/notes/{note_id}")
def get_note_by_id(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return get_note_by_id_crud(db=db, note_id=note_id, owner=owner)


@router.put("/notes/{note_id}")
def update_note(note_id: int, title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return update_note_crud(db=db, note_id=note_id, title=title, content=content, owner=owner)


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return delete_note_crud(db=db, note_id=note_id, owner=owner)
