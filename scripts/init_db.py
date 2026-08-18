from dotenv import load_dotenv
load_dotenv()

from app.db.session import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")