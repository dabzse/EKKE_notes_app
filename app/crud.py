from sqlalchemy.orm import Session
from .models import Note


def get_note_by_id(db: Session, note_id: int, user_id: int):
    return db.query(Note).filter(Note.id == note_id, Note.owner_id == user_id).first()


def create_note(db: Session, title: str, content: str, user_id: int):
    note = Note(title=title, content=content, owner_id=user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes(db: Session, user_id: int):
    return db.query(Note).filter(Note.owner_id == user_id).all()


def update_note(db: Session, note_id: int, title: str, content: str, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user_id).first()
    if note:
        note.title = title
        note.content = content
        db.commit()
        db.refresh(note)
    return note


def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note
