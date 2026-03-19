from app.db.base import Base
from app.db.session import engine
from app.models import user, disease, crop  # Import all models to register metadata

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
