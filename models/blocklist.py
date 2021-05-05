from extensions.db import db

class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklists"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
