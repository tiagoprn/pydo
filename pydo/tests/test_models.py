from pydo.models import User, Task


def test_register_user_with_hashed_password_must_be_successful(db_session):
    data = {
        'username': 'jean_luc_picard',
        'email': 'jlp@startrek.com',
        'password': '12345678'
    }
    new_user = User().register(username=data['username'], email=data['email'], password=data['password'])
    assert new_user.uuid
    assert new_user.password_hash != data['password']

def test_update_user(db_session):
    ...

def test_check_password(db_session):
    ...
