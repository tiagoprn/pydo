from pydo.models import User, Task


class TestUserModel:
    user_data = {
        'username': 'jean_luc_picard',
        'email': 'jlp@startrek.com',
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
        assert new_user.password_hash != self.user_data['password']

        is_same_password = new_user.check_password(password='12345678')
        assert is_same_password is True

    def test_get_by_uuid_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.uuid

        existing_user = User.get_by(uuid=str(new_user.uuid))
        assert existing_user.username == 'jean_luc_picard'

    def test_get_by_email_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.email

        existing_user = User.get_by(email='jlp@startrek.com')
        assert existing_user.username == 'jean_luc_picard'

    def test_get_by_username_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.username

        existing_user = User.get_by(username='jean_luc_picard')
        assert existing_user.email == 'jlp@startrek.com'

    def test_update_user_with_new_email_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.username

        old_email = new_user.email
        old_last_updated_at = new_user.last_updated_at
        new_email = 'jlp2@startrek.com'
        new_user.update(email=new_email)

        assert new_user.email == new_email

        assert new_user.last_updated_at > old_last_updated_at

    def test_update_user_with_new_password_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.username

        old_password = new_user.password_hash
        old_last_updated_at = new_user.last_updated_at
        new_password = '87654321'
        new_user.update(password=new_password)

        assert new_user.password_hash != old_password
        is_new_password = new_user.check_password(password=new_password)
        assert is_new_password is True

        assert new_user.last_updated_at > old_last_updated_at

    def test_update_user_with_new_email_and_new_password_must_be_successful(self, db_session):
        new_user = self.create_user()
        assert new_user.username

        old_email = new_user.email
        old_password = new_user.password_hash
        old_last_updated_at = new_user.last_updated_at
        new_email = 'jlp2@startrek.com'
        new_password = '87654321'
        new_user.update(email=new_email, password=new_password)

        assert new_user.email == new_email

        assert new_user.password_hash != old_password
        is_new_password = new_user.check_password(password=new_password)
        assert is_new_password is True

        assert new_user.last_updated_at > old_last_updated_at

    def test_update_user_with_no_params_must_not_change_properties(self, db_session):
        new_user = self.create_user()
        assert new_user.username

        old_email = new_user.email
        old_password = new_user.password_hash
        old_last_updated_at = new_user.last_updated_at
        new_user.update()

        assert new_user.email == old_email

        assert new_user.password_hash == old_password
        is_same_password = new_user.check_password(password='12345678')
        assert is_same_password is True

        assert new_user.last_updated_at == old_last_updated_at
