from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth.auth_service import decode_access_token
from ..crud import get_note_by_id as get_note_by_id_crud, create_note as create_note_crud, get_notes as get_notes_crud, update_note as update_note_crud, delete_note as delete_note_crud


router = APIRouter()

ERROR_401 = HTTPException(status_code=401, detail="Invalid token")

@router.post("/")
def create_note(title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    user_id = payload.get("sub")
    return create_note_crud(db=db, title=title, content=content, user_id=user_id)


@router.get("/")
def get_notes(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    user_id = payload.get("sub")
    notes = get_notes_crud(db=db, user_id=user_id)
    if not notes:
        print(f"No notes found for user_id: {user_id}")
    return notes


@router.get("/{note_id}")
def get_note_by_id(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    user_id = payload.get("sub")
    return get_note_by_id_crud(db=db, note_id=note_id, user_id=user_id)


@router.put("/{note_id}")
def update_note(note_id: int, title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    user_id = payload.get("sub")
    return update_note_crud(db=db, note_id=note_id, title=title, content=content, user_id=user_id)


@router.delete("/{note_id}")
def delete_note(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise ERROR_401
    user_id = payload.get("sub")
    return delete_note_crud(db=db, note_id=note_id, user_id=user_id)
