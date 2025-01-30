import random

from faker import Faker
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import User, Note
from app.auth.auth_service import hash_password

fake = Faker()

def create_fake_users_and_notes(
        db: Session, num_users: int = 10,
        max_notes_per_user: int = 5
):
    users = []
    notes = []

    with open("fake_data.txt", "a") as f:
        for _ in range(num_users):
            username = fake.user_name()
            plain_password = fake.password()
            hashed_password = hash_password(plain_password)
            user = User(username=username, hashed_password=hashed_password)
            db.add(user)
            db.commit()
            db.refresh(user)
            users.append(user)

            f.write(f"Username: {username}, Password: {plain_password}\n")

    for user in users:
        num_notes = random.randint(1, max_notes_per_user)
        for _ in range(num_notes):
            note = Note(title=fake.sentence(), content=fake.text(), owner=user.username)
            notes.append(note)

    random.shuffle(notes)
    db.add_all(notes)
    db.commit()

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    create_fake_users_and_notes(db)
    db.close()
    print("Fake data created successfully")
