from datetime import datetime
from typing import Dict
from unittest import mock

from pydo.models import User, Task
from pydo.tests.utils import create_tasks_for_various_users


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
            'password': '12345678',
        }

        response = test_client.post('/user', json=payload)
        return response

    def submit_login_request(
        self, test_client, email: str = 'jlp@startrek.com', password: str = '12345678'
    ):
        payload = {'email': email, 'password': password}

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
            'email': user_instance.email,
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
        payload = {'email': new_email, 'password': new_password}
        update_response = test_client.patch('/user', headers=headers, json=payload)
        assert update_response.status_code == 200

        expected_json_response = {
            'email': new_email,
            'password': 'SUCCESSFULLY CHANGED',
            'uuid': new_user_uuid,
        }
        assert update_response.json == expected_json_response

        user_instance = User.get_by(email=new_email)
        assert str(user_instance.uuid) == new_user_uuid

        # re-attempt login with updated email and password should get new access token
        new_login_response = self.submit_login_request(
            test_client=test_client, email=new_email, password=new_password
        )
        assert new_login_response.status_code == 200

        new_access_token = new_login_response.json['access_token']
        assert new_access_token is not None
        assert new_access_token != access_token


class TestTaskAPI:
    def submit_create_user_request(
        self,
        test_client,
        username: str = 'jean_luc_picard',
        email: str = 'jlp@startrek.com',
        password: str = '12345678',
    ):
        payload = {'username': username, 'email': email, 'password': password}

        response = test_client.post('/user', json=payload)
        return response

    def submit_login_request(
        self, test_client, email: str = 'jlp@startrek.com', password: str = '12345678'
    ):
        payload = {'email': email, 'password': password}

        response = test_client.post('/login', json=payload)
        return response

    def create_user_and_login(self, test_client, db_session) -> Dict:
        create_user_response = self.submit_create_user_request(test_client=test_client)
        new_user_uuid = create_user_response.json['uuid']

        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        return {'user_uuid': new_user_uuid, 'request_headers': headers}

    def test_create_task_successfully_for_current_user_through_api(
        self, test_client, db_session
    ):
        """
        When user_uuid is not specified on the payload, I create the task for the logged user_uuid
        """
        user_info = self.create_user_and_login(
            test_client=test_client, db_session=db_session
        )
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        payload = {
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00',
        }
        create_response = test_client.post(
            '/task', headers=request_headers, json=payload
        )
        assert create_response.status_code == 201

        response_data = create_response.json

        expected_response = {
            'description': 'Mathematics 101',
            'due_date': '2025-03-31T11:00:00',
            'status': 'pending',
            'title': 'Study for the test',
            'user_uuid': user_uuid,
        }

        assert response_data.pop('created_at') is not None
        assert response_data.pop('last_updated_at') is not None
        assert response_data.pop('uuid') is not None
        assert response_data == expected_response

    def test_create_task_successfully_for_another_user_through_api(
        self, test_client, db_session
    ):
        """
        When user_uuid is specified on the payload, I create the task for that user_uuid
        """
        #
        user_info = self.create_user_and_login(
            test_client=test_client, db_session=db_session
        )
        request_headers = user_info['request_headers']

        user_uuid_to_assign_to_response = self.submit_create_user_request(
            test_client=test_client,
            username='deanna_troy',
            email='dt@startrek.com',
            password='87654321',
        )

        user_uuid_to_assign_to = user_uuid_to_assign_to_response.json['uuid']

        payload = {
            'user_uuid': user_uuid_to_assign_to,
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00',
        }
        create_response = test_client.post(
            '/task', headers=request_headers, json=payload
        )
        assert create_response.status_code == 201

        response_data = create_response.json

        expected_response = {
            'description': 'Mathematics 101',
            'due_date': '2025-03-31T11:00:00',
            'status': 'pending',
            'title': 'Study for the test',
            'user_uuid': user_uuid_to_assign_to,
        }

        assert response_data.pop('created_at') is not None
        assert response_data.pop('last_updated_at') is not None
        assert response_data.pop('uuid') is not None
        assert response_data == expected_response

    def test_update_task_successfully_with_no_task_user_reassign_through_api(
        self, test_client, db_session
    ):
        user_info = self.create_user_and_login(
            test_client=test_client, db_session=db_session
        )
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        create_payload = {
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00',
        }
        create_response = test_client.post(
            '/task', headers=request_headers, json=create_payload
        )
        assert create_response.status_code == 201

        payload = {
            'uuid': create_response.json['uuid'],
            'title': 'Study for the test * updated',
            'description': 'Mathematics 101 * updated',
            'due_date': '2025-03-31 11:30',
            'status': 'completed',
        }
        update_response = test_client.patch(
            '/task', headers=request_headers, json=payload
        )
        assert update_response.status_code == 200

        response_data = update_response.json

        expected_response = {
            'uuid': create_response.json['uuid'],
            'description': 'Mathematics 101 * updated',
            'due_date': '2025-03-31T11:30:00',
            'status': 'completed',
            'title': 'Study for the test * updated',
            'user_uuid': user_uuid,
        }
        assert response_data.pop('created_at') is not None
        assert response_data.pop('last_updated_at') is not None
        assert response_data == expected_response

    def test_update_task_successfully_with_task_user_reassign_through_api(
        self, test_client, db_session
    ):
        user_info = self.create_user_and_login(
            test_client=test_client, db_session=db_session
        )
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        create_payload = {
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00',
        }
        create_response = test_client.post(
            '/task', headers=request_headers, json=create_payload
        )
        assert create_response.status_code == 201

        user_uuid_to_assign_to_response = self.submit_create_user_request(
            test_client=test_client,
            username='deanna_troy',
            email='dt@startrek.com',
            password='87654321',
        )

        user_uuid_to_assign_to = user_uuid_to_assign_to_response.json['uuid']

        payload = {
            'uuid': create_response.json['uuid'],
            'title': 'Study for the test * updated',
            'description': 'Mathematics 101 * updated',
            'due_date': '2025-03-31 11:30',
            'status': 'completed',
            'user_uuid': user_uuid_to_assign_to,
        }
        update_response = test_client.patch(
            '/task', headers=request_headers, json=payload
        )
        assert update_response.status_code == 200

        response_data = update_response.json

        expected_response = {
            'uuid': create_response.json['uuid'],
            'description': 'Mathematics 101 * updated',
            'due_date': '2025-03-31T11:30:00',
            'status': 'completed',
            'title': 'Study for the test * updated',
            'user_uuid': user_uuid_to_assign_to,
        }
        assert response_data.pop('created_at') is not None
        assert response_data.pop('last_updated_at') is not None
        assert response_data == expected_response

    def test_delete_task_successfully_through_api(self, test_client, db_session):
        user_info = self.create_user_and_login(
            test_client=test_client, db_session=db_session
        )
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        create_payload = {
            'user_uuid': user_uuid,
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00',
        }
        create_response = test_client.post(
            '/task', headers=request_headers, json=create_payload
        )
        assert create_response.status_code == 201

        payload = {
            'uuid': create_response.json['uuid'],
        }
        response = test_client.delete('/task', headers=request_headers, json=payload)
        assert response.status_code == 204
        assert response.text == ''

    def test_get_task_successfully_through_api(self, test_client, db_session):
        user_info = self.create_user_and_login(
            test_client=test_client, db_session=db_session
        )
        user_uuid = user_info['user_uuid']
        request_headers = user_info['request_headers']

        create_payload = {
            'user_uuid': user_uuid,
            'title': 'Study for the test',
            'description': 'Mathematics 101',
            'due_date': '2025-03-31 11:00',
        }
        create_response = test_client.post(
            '/task', headers=request_headers, json=create_payload
        )
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

    def test_get_tasks_with_filters_for_single_user_must_retrieve_correct_tasks(
        self, test_client, db_session
    ):
        # GIVEN
        uuids = create_tasks_for_various_users()
        assert len(uuids) == 15

        first_user = User.get_by(username='jean_luc_picard')

        filter_query_params = {
            'user_uuids': [first_user.uuid],
            'status': ['pending', 'in_progress'],
            'start_due_date': datetime.strptime('2025-01-02 00:00', '%Y-%m-%d %H:%M'),
            'end_due_date': datetime.strptime('2025-01-04 23:59', '%Y-%m-%d %H:%M'),
        }
        jean_luc_picard_tasks = Task.filter_by(**filter_query_params)

        expected_uuids_values = {uuids[0], uuids[1]}
        uuid_values = {str(task.uuid) for task in jean_luc_picard_tasks}
        assert uuid_values == expected_uuids_values

        # WHEN
        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        request_params = {
            'user_uuids': [first_user.uuid],
            'status': ['pending', 'in_progress'],
            'start_due_date': '2025-01-02 00:00',
            'end_due_date': '2025-01-04 23:59',
        }
        get_response = test_client.get('/tasks', headers=headers, json=request_params)
        assert get_response.status_code == 200

        # THEN
        response_data = get_response.json

        assert len(response_data) == 2
        response_uuids = []
        for record in response_data:
            expected_keys = {
                'created_at',
                'description',
                'due_date',
                'last_updated_at',
                'status',
                'title',
                'user_name',
                'user_uuid',
                'uuid',
            }
            assert set(record.keys()) == expected_keys
            for key in expected_keys:
                record[key] is not None

            response_uuids.append(record.pop('uuid'))

        assert set(response_uuids) == expected_uuids_values

    def test_get_tasks_with_filters_for_multi_users_must_retrieve_correct_tasks(
        self, test_client, db_session
    ):
        # GIVEN
        uuids = create_tasks_for_various_users()
        assert len(uuids) == 15

        first_user = User.get_by(username='jean_luc_picard')
        second_user = User.get_by(username='william_riker')
        third_user = User.get_by(username='deanna_troy')

        filter_query_params = {
            'user_uuids': [first_user.uuid, second_user.uuid, third_user.uuid],
            'status': ['completed'],
            'start_due_date': datetime.strptime('2025-01-02 13:00', '%Y-%m-%d  %H:%M'),
            'end_due_date': datetime.strptime('2025-01-06 10:20', '%Y-%m-%d %H:%M'),
        }

        multi_user_tasks = Task.filter_by(**filter_query_params)

        expected_uuids_values = {uuids[4], uuids[6], uuids[12]}
        uuid_values = {str(task.uuid) for task in multi_user_tasks}
        assert uuid_values == expected_uuids_values

        # WHEN
        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        request_params = {
            'user_uuids': [first_user.uuid, second_user.uuid, third_user.uuid],
            'status': ['completed'],
            'start_due_date': '2025-01-02 13:00',
            'end_due_date': '2025-01-06 10:20',
        }
        get_response = test_client.get('/tasks', headers=headers, json=request_params)
        assert get_response.status_code == 200

        # THEN
        response_data = get_response.json

        assert len(response_data) == 3
        response_uuids = []
        for record in response_data:
            expected_keys = {
                'created_at',
                'description',
                'due_date',
                'last_updated_at',
                'status',
                'title',
                'user_name',
                'user_uuid',
                'uuid',
            }
            assert set(record.keys()) == expected_keys
            for key in expected_keys:
                record[key] is not None

            response_uuids.append(record.pop('uuid'))

        assert set(response_uuids) == expected_uuids_values

    def test_get_tasks_with_no_filters_must_retrieve_all_tasks(
        self, test_client, db_session
    ):
        # GIVEN
        uuids = create_tasks_for_various_users()
        assert len(uuids) == 15

        # WHEN
        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        request_params = {
            'user_uuids': [],
            'status': [],
            'start_due_date': '',
            'end_due_date': '',
        }
        get_response = test_client.get('/tasks', headers=headers, json=request_params)
        assert get_response.status_code == 200

        # THEN
        response_data = get_response.json

        assert len(response_data) == 15
        response_uuids = []
        for record in response_data:
            expected_keys = {
                'created_at',
                'description',
                'due_date',
                'last_updated_at',
                'status',
                'title',
                'user_name',
                'user_uuid',
                'uuid',
            }
            assert set(record.keys()) == expected_keys
            for key in expected_keys:
                record[key] is not None

            response_uuids.append(record.pop('uuid'))

        assert set(response_uuids) == set(uuids)

    def test_get_tasks_with_no_filters_and_pagination_must_retrieve_page_tasks(
        self, test_client, db_session
    ):
        # GIVEN
        uuids = create_tasks_for_various_users()
        assert len(uuids) == 15

        # WHEN
        login_response = self.submit_login_request(test_client=test_client)
        access_token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        request_params = {
            'user_uuids': [],
            'status': [],
            'start_due_date': '',
            'end_due_date': '',
            'page_number': 2,
        }
        get_response = test_client.get('/tasks', headers=headers, json=request_params)
        assert get_response.status_code == 200

        # THEN
        response_data = get_response.json

        assert response_data['current_page'] == 2
        assert response_data['has_next'] is True
        assert response_data['has_prev'] is True
        assert response_data['total_pages'] == 3

        records = response_data['records']
        assert len(records) == 5

        response_uuids = []
        for record in records:
            expected_keys = {
                'created_at',
                'description',
                'due_date',
                'last_updated_at',
                'status',
                'title',
                'user_name',
                'user_uuid',
                'uuid',
            }
            assert set(record.keys()) == expected_keys
            for key in expected_keys:
                record[key] is not None

            response_uuids.append(record.pop('uuid'))
