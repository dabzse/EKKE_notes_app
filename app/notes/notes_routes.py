from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.auth_service import decode_access_token
from app.models import User
from app.schemas import Note
from app.notes.notes_service import (
    create_note_service,
    get_notes_service,
    get_note_by_id_service,
    update_note_service,
    delete_note_service,
)

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
        payload = jwt.decode(
            token,
            "222adc0c77257f628b56c5502b6b2e2b5018d95cb7efbc1ebb50657f26faac49",
            algorithms=["HS256"]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/notes", response_model=Note)
async def create_note(title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return create_note_service(db=db, title=title, content=content, owner=owner)


@router.get("/notes", response_class=HTMLResponse)
def get_notes(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = get_notes_service(db, current_user.username)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})


@router.get("/notes/{note_id}")
def get_note_by_id(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return get_note_by_id_service(db=db, note_id=note_id, owner=owner)


'''
this will give you an error because of the current_user dependency:
    the issue might be that the token is not being properly decoded or validated

I looked after the error and I didn't find the correct answer

@router.get("/notes/{note_id}")
def get_note_by_id(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = get_note_by_id_service(db=db, note_id=note_id, owner=current_user.username)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
'''


@router.put("/notes/{note_id}")
def update_note(note_id: int, title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return update_note_service(db=db, note_id=note_id, title=title, content=content, owner=owner)


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    owner = payload.get("sub")
    return delete_note_service(db=db, note_id=note_id, owner=owner)
