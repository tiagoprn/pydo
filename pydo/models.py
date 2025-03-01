from datetime import datetime
from typing import List, Union
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

    def hash(self, password: str) -> object:
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def register(self, username: str, email: str, password: str) -> 'User':
        hashed_password = self.hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return new_user

    @staticmethod
    def get_by(uuid: str='', email: str='', username: str='') -> Union[None, "User"]:
        if uuid:
            return User.query.filter_by(uuid=uuid).first()
        if email:
            return User.query.filter_by(email=email).first()
        if username:
            return User.query.filter_by(username=username).first()
        return None

    def update(self, uuid: str, email: str='', password: str=''):
        ...  # TODO:
        self.last_updated_at = datetime.utcnow()



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

    def filter_by(self, user_uuid: str, status: List[str], due_date: datetime):
        ...  # TODO:
