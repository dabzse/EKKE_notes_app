from sqlalchemy.orm import Session
from app.crud import (
    create_note as create_note_crud,
    get_notes as get_notes_crud,
    get_note_by_id as get_note_by_id_crud,
    update_note as update_note_crud,
    delete_note as delete_note_crud,
)


def create_note_service(db: Session, title: str, content: str, owner: str):
    return create_note_crud(db=db, title=title, content=content, owner=owner)


def get_notes_service(db: Session, owner: str):
    return get_notes_crud(db, owner)


def get_note_by_id_service(db: Session, note_id: int, owner: str):
    return get_note_by_id_crud(db=db, note_id=note_id, owner=owner)


def update_note_service(db: Session, note_id: int, title: str, content: str, owner: str):
    return update_note_crud(db=db, note_id=note_id, title=title, content=content, owner=owner)


def delete_note_service(db: Session, note_id: int, owner: str):
    return delete_note_crud(db=db, note_id=note_id, owner=owner)
