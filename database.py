from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Models
class ModelUser(db.Model):
    __tablename__ = "Users"

    ID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.Text)
    Hash = db.Column(db.Text)
    Role = db.Column(db.Text)
    Wins = db.Column(db.Integer)
    Losses = db.Column(db.Integer)
