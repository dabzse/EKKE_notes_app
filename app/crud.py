from sqlalchemy.orm import Session
from app.models import Note, User

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_note(db: Session, title: str, content: str, owner: str):
    note = Note(title=title, content=content, owner=owner)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db: Session, owner: str):
    return db.query(Note).filter(Note.owner == owner).all()

def get_note_by_id(db: Session, note_id: int, owner: str):
    return db.query(Note).filter(Note.id == note_id, Note.owner == owner).first()

def update_note(db: Session, note_id: int, title: str, content: str, owner: str):
    note = db.query(Note).filter(Note.id == note_id, Note.owner == owner).first()
    if note:
        note.title = title
        note.content = content
        db.commit()
        db.refresh(note)
    return note

def delete_note(db: Session, note_id: int, owner: str):
    note = db.query(Note).filter(Note.id == note_id, Note.owner == owner).first()
    if note:
        db.delete(note)
        db.commit()
    return note