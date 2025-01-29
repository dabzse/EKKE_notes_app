from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..auth.auth_service import decode_access_token
from ..notes.notes_service import create_note, get_notes, get_note_by_id, update_note, delete_note

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_new_note(title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    return create_note(db=db, title=title, content=content, user_id=user_id)

@router.get("/")
def list_notes(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    return get_notes(db=db, user_id=user_id)

@router.get("/{note_id}")
def retrieve_note(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    return get_note_by_id(db=db, note_id=note_id, user_id=user_id)

@router.put("/{note_id}")
def update_existing_note(note_id: int, title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    return update_note(db=db, note_id=note_id, title=title, content=content, user_id=user_id)

@router.delete("/{note_id}")
def delete_existing_note(note_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    return delete_note(db=db, note_id=note_id, user_id=user_id)

