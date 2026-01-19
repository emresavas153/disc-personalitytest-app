# db.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class Host(db.Model):
    __tablename__ = "hosts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    workshops = db.relationship("Workshop", back_populates="host", cascade="all, delete-orphan")


class Workshop(db.Model):
    __tablename__ = "workshops"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="open")
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"), nullable=False)
    host = db.relationship("Host", back_populates="workshops")
