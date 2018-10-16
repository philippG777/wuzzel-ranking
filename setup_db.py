from app import app, db
db.create_all(app = app)
print("Created DB")
