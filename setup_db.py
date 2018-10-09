from database import db
from app import app
db.create_all(app = app)
print("Created DB")
