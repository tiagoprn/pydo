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
        new_user = User(username=username, email=email, password_hash=self.hash(password))
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return new_user

    def update(self, email: str='', password: str=''):
        if (not email) and (not password):
            return self

        if email:
            self.email = email

        if password:
            self.password_hash = self.hash(password)

        self.last_updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    @staticmethod
    def get_by(uuid: str='', email: str='', username: str='') -> Union[None, "User"]:
        if uuid:
            return User.query.filter_by(uuid=uuid).first()
        if email:
            return User.query.filter_by(email=email).first()
        if username:
            return User.query.filter_by(username=username).first()
        return None


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

    def create(self, user_uuid: str, title: str, description: str, status: str, due_date: datetime=None) -> 'Task':
        data = {
            'user_uuid': user_uuid,
            'title': title,
            'description': description,
            'status': status
        }
        if due_date:
            data['due_date'] = due_date
        new_task = Task(**data)
        db.session.add(new_task)
        db.session.commit()
        db.session.refresh(new_task)
        return new_task

    def update(self, title: str='', description: str='', status: str='', due_date: datetime=None):
        if not(title or description or status or due_date):
            return

        if title:
            self.title = title

        if description:
            self.description = description

        if status:
            self.status = status

        if self.due_date:
            self.due_date = due_date

        self.last_updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    @staticmethod
    def filter_by(user_uuids: List[str]=[], uuids: List[str]=[], status: List[str]=[], due_date: datetime=None):
        filters_data = {}

        if user_uuids:
            filters_data['user_uuid'] = user_uuids[0]  # TODO: support list of user_uuids

        if uuids:
            filters_data['uuid'] = uuids[0]  # TODO: support list of uuids

        if status:
            filters_data['status'] = status

        if due_date:
            filters_data['due_date'] = due_date  # TODO: add start_due_date & end_due_date

        print(f'>>>>>> filters: {filters_data}')

        return Task.query.filter_by(**filters_data).all()
