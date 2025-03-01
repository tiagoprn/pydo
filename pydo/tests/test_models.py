from pydo.models import User, Task


class TestUserModel:
    user_data = {
        'username': 'jean_luc_picarde',
        'email': 'jlpe@startrek.com',
        'password': '12345678'
    }

    def create_user(self):
        new_user = User().register(username=self.user_data['username'],
                                   email=self.user_data['email'],
                                   password=self.user_data['password'])
        return new_user

    def test_register_user_with_hashed_password_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.uuid
        print(new_user.uuid)
        assert new_user.password_hash != self.user_data['password']

    def test_get_by_uuid_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.uuid
        print(new_user.uuid)
        # TODO: make the assertion

    def test_update_user(db_session):
        ...

    def test_check_password(db_session):
        ...
