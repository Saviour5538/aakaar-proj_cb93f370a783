import uuid
from datetime import datetime
from database.models import Base, engine, SessionLocal, User, Document, Chunk, Conversation, Message

def seed_database():
    session = SessionLocal()
    try:
        # Clear existing data
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # Seed Users
        user1 = User(
            id=str(uuid.uuid4()),
            email="alice@example.com",
            password_hash="hashed_password_1",
            role="admin",
            created_at=datetime(2023, 10, 1, 12, 0, 0)
        )
        user2 = User(
            id=str(uuid.uuid4()),
            email="bob@example.com",
            password_hash="hashed_password_2",
            role="user",
            created_at=datetime(2023, 10, 2, 12, 0, 0)
        )
        session.add_all([user1, user2])

        # Seed Documents
        document1 = Document(
            id=str(uuid.uuid4()),
            user_id=user1.id,
            filename="example.pdf",
            status="processed",
            chunk_count=5,
            created_at=datetime(2023, 10, 3, 12, 0, 0)
        )
        document2 = Document(
            id=str(uuid.uuid4()),
            user_id=user2.id,
            filename="example.docx",
            status="pending",
            chunk_count=None,
            created_at=datetime(2023, 10, 4, 12, 0, 0)
        )
        session.add_all([document1, document2])

        # Commit changes
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()