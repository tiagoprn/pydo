from datetime import datetime
from uuid import uuid4

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from pydo.extensions import db, bcrypt

"""
Available datatypes:
https://docs.sqlalchemy.org/en/13/core/type_basics.html
"""


class User(db.Model):
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        self.last_updated_at = datetime.utcnow()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)


class Task(db.Model):
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        Enum('pending', 'in_progress', 'completed', name='task_status_enum'),
        default='pending',
        nullable=False,
    )
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("user.uuid"), nullable=False)
