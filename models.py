from datetime import datetime
from db import db

class Host(db.Model):
    __tablename__ = "hosts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    workshops = db.relationship("Workshop", back_populates="host", cascade="all, delete-orphan")


class Workshop(db.Model):
    __tablename__ = "workshops"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="open", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"), nullable=False)
    host = db.relationship("Host", back_populates="workshops")

    participants = db.relationship("Participant", back_populates="workshop", cascade="all, delete-orphan")
    answers = db.relationship("Answer", back_populates="workshop", cascade="all, delete-orphan")



class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    participant_token = db.Column(db.String(64), unique=True, nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"), nullable=False)
    workshop = db.relationship("Workshop", back_populates="participants")

    answers = db.relationship("Answer", back_populates="participant", cascade="all, delete-orphan")



class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    dimension = db.Column(db.String(1), nullable=False)

    answers = db.relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=False)
    participant = db.relationship("Participant", back_populates="answers")

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    question = db.relationship("Question", back_populates="answers")

    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"), nullable=False)
    workshop = db.relationship("Workshop", back_populates="answers")

