import pytest

from pydo.factory import create_app
from pydo.extensions import db

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app  # This ensures the app context is active during tests

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()  # Clean up after each test
