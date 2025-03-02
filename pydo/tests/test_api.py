from typing import Dict
from unittest import mock

from pydo.models import User, Task


def test_compute_sent_to_queue(test_client):
    response = test_client.get('/compute')
    assert response.status_code == 200
    assert response.json == {'message': 'Successfully sent to queue.'}


def test_404(test_client):
    response = test_client.get('/api/echoes')
    assert response.status_code == 404


@mock.patch('pydo.commons.get_app_version', return_value='1.0')
def test_healthcheck_readiness(_mocked_version, test_client):
    response = test_client.get('/health-check/readiness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'ready', 'app_version', 'app_type'}


@mock.patch('pydo.commons.get_app_version', return_value='1.0')
def test_healthcheck_liveness(_mocked_version, test_client):
    response = test_client.get('/health-check/liveness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'live', 'version', 'timestamp'}


class TestUserAPI:
    def submit_create_user_request(self, test_client):
        payload = {
            'username': 'jean_luc_picard',
            'email': 'jlp@startrek.com',
            'password': '12345678'
        }

        response = test_client.post('/user', json=payload)
        return response

    def submit_login_request(self, test_client, email: str='jlp@startrek.com', password: str='12345678'):
        payload = {
            'email': email,
            'password': password
        }

        response = test_client.post('/login', json=payload)
        return response

    def test_create_user(self, test_client, db_session):
        response = self.submit_create_user_request(test_client=test_client)
        assert response.status_code == 201

        new_user_uuid = response.json['uuid']
        assert isinstance(new_user_uuid, str)

    def test_login_successful(self, test_client, db_session):
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        assert login_response.status_code == 200

        access_token = login_response.json['access_token']
        refresh_token = login_response.json['refresh_token']

        assert access_token is not None
        assert refresh_token is not None

    def test_get_user_data_after_login(self, test_client, db_session):
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']
        refresh_token = login_response.json['refresh_token']

        headers = {'Authorization': f'Bearer {access_token}'}
        response = test_client.get('/user', headers=headers)
        assert response.status_code == 200

        user_instance = User.get_by(uuid=new_user_uuid)

        expected_json_response = {
            'uuid': str(user_instance.uuid),
            'username': user_instance.username,
            'email': user_instance.email
        }
        assert response.json == expected_json_response

    def test_get_new_jwt_temporary_token_when_logged_in(self, test_client, db_session):
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        assert login_response.status_code == 200

        access_token = login_response.json['access_token']
        refresh_token = login_response.json['refresh_token']

        headers = {'Authorization': f'Bearer {refresh_token}'}
        response = test_client.post('/token/new', headers=headers)
        assert response.status_code == 200

        new_access_token = response.json['access_token']
        assert new_access_token is not None
        assert new_access_token != access_token

    def test_update_user_successfully(self, test_client, db_session):
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']

        headers = {'Authorization': f'Bearer {access_token}'}
        new_email = 'jean_luc_picard.captain@startrek.com'
        new_password = 'resistance-is-futile'
        payload = {
            'email': new_email,
            'password': new_password
        }
        update_response = test_client.patch('/user', headers=headers, json=payload)
        assert update_response.status_code == 200

        expected_json_response = {
            'email': new_email,
            'password': 'SUCCESSFULLY CHANGED',
            'uuid': new_user_uuid
        }
        assert update_response.json == expected_json_response

        user_instance = User.get_by(email=new_email)
        assert str(user_instance.uuid) == new_user_uuid

        # re-attempt login with updated email and password should get new access token
        new_login_response = self.submit_login_request(test_client=test_client, email=new_email, password=new_password)
        assert new_login_response.status_code == 200

        new_access_token = new_login_response.json['access_token']
        assert new_access_token is not None
        assert new_access_token != access_token


class TestTaskAPI():
    def submit_create_user_request(self, test_client):
        payload = {
            'username': 'jean_luc_picard',
            'email': 'jlp@startrek.com',
            'password': '12345678'
        }

        response = test_client.post('/user', json=payload)
        return response

    def submit_login_request(self, test_client, email: str='jlp@startrek.com', password: str='12345678'):
        payload = {
            'email': email,
            'password': password
        }

        response = test_client.post('/login', json=payload)
        return response

    def create_user_and_login(self, test_client, db_session) -> Dict:
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        return {'user_uuid': new_user_uuid, 'request_headers': headers}

    def test_create_task_successfully_through_api(self, test_client, db_session):
        user_info = self.create_user_and_login(test_client=test_client, db_session=db_session)
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        payload = {
            'user_uuid': user_uuid,
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00'
        }
        create_response = test_client.post('/task', headers=request_headers, json=payload)
        assert create_response.status_code == 201

        response_data = create_response.json

        expected_response = {
            'description': 'Mathematics 101',
            'due_date': '2025-03-31T11:00:00',
            'status': 'pending',
            'title': 'Study for the test',
        }

        assert response_data.pop('created_at') is not None
        assert response_data.pop('last_updated_at') is not None
        assert response_data.pop('uuid') is not None
        assert response_data == expected_response

    def test_update_task_successfully_through_api(self, test_client, db_session):
        user_info = self.create_user_and_login(test_client=test_client, db_session=db_session)
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        create_payload = {
            'user_uuid': user_uuid,
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00'
        }
        create_response = test_client.post('/task', headers=request_headers, json=create_payload)
        assert create_response.status_code == 201

        payload = {
            'uuid': create_response.json['uuid'],
            'title': 'Study for the test * updated',
            'description': 'Mathematics 101 * updated',
            'due_date': '2025-03-31 11:30',
            'status': 'completed'
        }
        update_response = test_client.patch('/task', headers=request_headers, json=payload)
        assert update_response.status_code == 200

        response_data = update_response.json

        expected_response = {
            'uuid': create_response.json['uuid'],
            'description': 'Mathematics 101 * updated',
            'due_date': '2025-03-31T11:30:00',
            'status': 'completed',
            'title': 'Study for the test * updated',
        }
        assert response_data.pop('created_at') is not None
        assert response_data.pop('last_updated_at') is not None
        assert response_data == expected_response

    def test_delete_task_successfully_through_api(self, test_client, db_session):
        user_info = self.create_user_and_login(test_client=test_client, db_session=db_session)
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        create_payload = {
            'user_uuid': user_uuid,
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00'
        }
        create_response = test_client.post('/task', headers=request_headers, json=create_payload)
        assert create_response.status_code == 201

        payload = {
            'uuid': create_response.json['uuid'],
        }
        response = test_client.delete('/task', headers=request_headers, json=payload)
        assert response.status_code == 204
        assert response.text == ''

    def test_get_task_successfully_through_api(self, test_client, db_session):
        user_info = self.create_user_and_login(test_client=test_client, db_session=db_session)
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        create_payload = {
            'user_uuid': user_uuid,
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00'
        }
        create_response = test_client.post('/task', headers=request_headers, json=create_payload)
        assert create_response.status_code == 201

        payload = {
            'uuid': create_response.json['uuid'],
        }
        get_response = test_client.get('/task', headers=request_headers, json=payload)
        assert get_response.status_code == 200

        response_data = get_response.json

        expected_response = {
            'uuid': create_response.json['uuid'],
            'description': 'Mathematics 101',
            'due_date': '2025-03-31T11:00:00',
            'status': 'pending',
            'title': 'Study for the test',
        }
        assert response_data.pop('created_at') is not None
        assert response_data.pop('last_updated_at') is not None
        assert response_data == expected_response
