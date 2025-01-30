from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Note
from ..auth.auth_service import decode_access_token

router = APIRouter()

@router.post("/notes")
def create_note(title: str, content: str, token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    note = Note(title=title, content=content, owner_id=payload["sub"])
    db.add(note)
    db.commit()
    return note
