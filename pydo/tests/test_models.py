from datetime import datetime, timedelta
from typing import List

import pytest
from sqlalchemy.exc import DataError

from pydo.models import User, Task

# TODO: the functions below could be fixtures on conftest.py
def create_user():
    user_data = {
        'username': 'jean_luc_picard',
        'email': 'jlp@startrek.com',
        'password': '12345678'
    }
    new_user = User().register(**user_data)
    return new_user

def create_tasks_for_single_user(status: List[str]=[]) -> List[str]:
    uuids = []

    user = create_user()

    tasks_data = [
        {
            'user_uuid': user.uuid,
            'title': 'study',
            'description': 'must get better',
            'due_date': datetime.utcnow() + timedelta(days=3),
            'status': status[0] if status else 'pending'
        },
        {
            'user_uuid': user.uuid,
            'title': 'gym',
            'description': 'must get healthy',
            'due_date': datetime.utcnow() + timedelta(days=1),
            'status': status[1] if status else 'pending'
        },
    ]
    for data in tasks_data:
        new_task = Task().create(**data)
        uuids.append(str(new_task.uuid))

    return uuids

def create_multi_users():
    created_users = []
    users_data = [
        {
            'username': 'jean_luc_picard',
            'email': 'jlp@startrek.com',
            'password': '12345678'
        },
        {
            'username': 'william_riker',
            'email': 'wk@startrek.com',
            'password': '12345678'
        },
        {
            'username': 'deanna_troy',
            'email': 'dt@startrek.com',
            'password': '12345678'
        },
    ]
    for data in users_data:
        new_user = User().register(**data)
        created_users.append(new_user)
    return created_users


def create_tasks_for_various_users(status: List[str]=[]) -> List[str]:
    uuids = []

    users_pool = create_multi_users()
    first_user = users_pool[0]
    second_user = users_pool[1]
    third_user = users_pool[2]

    # Create 5 tasks for each user with varied properties
    # Fixed reference date: January 1st, 2025, 8AM UTC
    reference_date = datetime(2025, 1, 1, 8, 0, 0)

    """
    all users
    status=['completed'],
    start_due_date= datetime.strptime('2025-01-02', '%Y-%m-%d'),
    end_due_date= datetime.strptime('2025-01-04', '%Y-%m-%d'))

    indexes:
        4 - # Jan 3, 2025, 9:30 UTC
        6 - # Jan 2, 2025, 13:00 UTC
        12 - # Jan 6, 2025, 10:20 UTC
    """

    tasks_data = [
        # First user's tasks
        {  # 0
            'user_uuid': first_user.uuid,
            'title': 'Study',
            'description': 'Must get better at math',
            'due_date': reference_date + timedelta(days=3, hours=6, minutes=30),  # Jan 4, 2025, 14:30 UTC
            'status': 'pending'
        },
        {  # 1
            'user_uuid': first_user.uuid,
            'title': 'Gym',
            'description': 'Leg day workout',
            'due_date': reference_date + timedelta(days=1, hours=2, minutes=15),  # Jan 2, 2025, 10:15 UTC
            'status': 'in_progress'
        },
        {  # 2
            'user_uuid': first_user.uuid,
            'title': 'Reading',
            'description': 'Finish chapter 5',
            'due_date': reference_date + timedelta(days=7, hours=12),  # Jan 8, 2025, 20:00 UTC
            'status': 'pending'
        },
        {  # 3
            'user_uuid': first_user.uuid,
            'title': 'Project',
            'description': 'Complete the presentation',
            'due_date': reference_date + timedelta(days=5, hours=9, minutes=45),  # Jan 6, 2025, 17:45 UTC
            'status': 'in_progress'
        },
        {  # 4
            'user_uuid': first_user.uuid,
            'title': 'Meeting',
            'description': 'Team sync-up',
            'due_date': reference_date + timedelta(days=2, hours=1, minutes=30),  # Jan 3, 2025, 9:30 UTC
            'status': 'completed'
        },

        # Second user's tasks
        {  # 5
            'user_uuid': second_user.uuid,
            'title': 'Coding',
            'description': 'Fix bugs in API',
            'due_date': reference_date + timedelta(days=4, hours=3, minutes=20),  # Jan 5, 2025, 11:20 UTC
            'status': 'pending'
        },
        {  # 6
            'user_uuid': second_user.uuid,
            'title': 'Shopping',
            'description': 'Buy groceries',
            'due_date': reference_date + timedelta(days=1, hours=5),  # Jan 2, 2025, 13:00 UTC
            'status': 'completed'
        },
        {  # 7
            'user_uuid': second_user.uuid,
            'title': 'Cleaning',
            'description': 'Clean the apartment',
            'due_date': reference_date + timedelta(days=2, hours=10, minutes=15),  # Jan 3, 2025, 18:15 UTC
            'status': 'in_progress'
        },
        {  # 8
            'user_uuid': second_user.uuid,
            'title': 'Meditation',
            'description': 'Morning routine',
            'due_date': reference_date + timedelta(hours=18, minutes=30),  # Jan 2, 2025, 2:30 UTC
            'status': 'pending'
        },
        {  # 9
            'user_uuid': second_user.uuid,
            'title': 'Study',
            'description': 'Learn new framework',
            'due_date': reference_date + timedelta(days=10, hours=7, minutes=45),  # Jan 11, 2025, 15:45 UTC
            'status': 'in_progress'
        },

        # Third user's tasks
        {  # 10
            'user_uuid': third_user.uuid,
            'title': 'Cooking',
            'description': 'Try new recipe',
            'due_date': reference_date + timedelta(days=3, hours=4, minutes=10),  # Jan 4, 2025, 12:10 UTC
            'status': 'pending'
        },
        {  # 11
            'user_uuid': third_user.uuid,
            'title': 'Project',
            'description': 'Finish milestone 2',
            'due_date': reference_date + timedelta(days=14, hours=11, minutes=30),  # Jan 15, 2025, 19:30 UTC
            'status': 'in_progress'
        },
        {  # 12
            'user_uuid': third_user.uuid,
            'title': 'Reading',
            'description': 'Read industry articles',
            'due_date': reference_date + timedelta(days=5, hours=2, minutes=20),  # Jan 6, 2025, 10:20 UTC
            'status': 'completed'
        },
        {  # 13
            'user_uuid': third_user.uuid,
            'title': 'Meeting',
            'description': 'Client presentation',
            'due_date': reference_date + timedelta(days=2, hours=8, minutes=45),  # Jan 3, 2025, 16:45 UTC
            'status': 'pending'
        },
        {  # 14
            'user_uuid': third_user.uuid,
            'title': 'Gym',
            'description': 'Cardio session',
            'due_date': reference_date + timedelta(days=1, hours=1, minutes=15),  # Jan 2, 2025, 9:15 UTC
            'status': 'in_progress'
        }
    ]

    for data in tasks_data:
        new_task = Task().create(**data)
        uuids.append(str(new_task.uuid))

    return uuids


class TestUserModel:
    def test_register_user_with_hashed_password_must_be_successful(self, db_session):
        new_user = create_user()
        assert new_user.uuid
        assert new_user.password_hash != '12345678'

        is_same_password = new_user.check_password(password='12345678')
        assert is_same_password is True

    def test_get_by_uuid_must_be_successful(self, db_session):
        new_user = create_user()
        assert new_user.uuid

        existing_user = User.get_by(uuid=str(new_user.uuid))
        assert existing_user.username == 'jean_luc_picard'

    def test_get_by_email_must_be_successful(self, db_session):
        new_user = create_user()
        assert new_user.email

        existing_user = User.get_by(email='jlp@startrek.com')
        assert existing_user.username == 'jean_luc_picard'

    def test_get_by_username_must_be_successful(self, db_session):
        new_user = create_user()
        assert new_user.username

        existing_user = User.get_by(username='jean_luc_picard')
        assert existing_user.email == 'jlp@startrek.com'

    def test_update_user_with_new_email_must_be_successful(self, db_session):
        new_user = create_user()
        assert new_user.username

        old_email = new_user.email
        old_last_updated_at = new_user.last_updated_at
        new_email = 'jlp2@startrek.com'
        new_user.update(email=new_email)

        assert new_user.email == new_email

        assert new_user.last_updated_at > old_last_updated_at

    def test_update_user_with_new_password_must_be_successful(self, db_session):
        new_user = create_user()
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
        new_user = create_user()
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
        new_user = create_user()
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


class TestTaskModel():
    def test_create_tasks_for_single_user_with_valid_status(self, db_session):
        tasks_uuids = create_tasks_for_single_user()
        print(f'tasks_uuids={tasks_uuids}')
        assert len(tasks_uuids) == 2

        created_tasks = Task.filter_by(uuids=tasks_uuids)
        assert len(created_tasks) == 2

    def test_do_not_create_task_with_invalid_status(self, db_session):
        tasks_uuids = None
        with pytest.raises(DataError) as exception_instance:
            tasks_uuids = create_tasks_for_single_user(status=['invalid1', 'invalid2'])

        assert tasks_uuids is None
        assert exception_instance.type is DataError
        expected_exception_value = ('(psycopg2.errors.InvalidTextRepresentation) invalid input value '
                                    'for enum task_status_enum: "invalid1"')
        assert expected_exception_value in exception_instance.value.args[0]

    def test_update_task_successfully(self, db_session):
        tasks_uuids = create_tasks_for_single_user()
        print(f'tasks_uuids={tasks_uuids}')
        assert len(tasks_uuids) == 2

        first_task = Task.filter_by(uuids=[tasks_uuids[0]])[0]
        assert first_task

        first_task_original_last_updated_at = first_task.last_updated_at

        update_values = {
            'title': 'changed title',
            'description': 'changed description',
            'status': 'in_progress',
            'due_date': datetime.utcnow() + timedelta(days=15)
        }
        first_task.update(**update_values)

        for expected_property, expected_value in update_values.items():
            value = getattr(first_task, expected_property)
            assert value == expected_value

        assert first_task.last_updated_at > first_task_original_last_updated_at

    def test_must_not_update_task_if_no_params_on_update(self, db_session):
        tasks_uuids = create_tasks_for_single_user()
        print(f'tasks_uuids={tasks_uuids}')
        assert len(tasks_uuids) == 2

        first_task = Task.filter_by(uuids=[tasks_uuids[0]])[0]
        assert first_task

        first_task_original_last_updated_at = first_task.last_updated_at

        update_values = {}
        first_task.update(**update_values)

        assert first_task.last_updated_at == first_task_original_last_updated_at

    def test_filters_must_get_correct_tasks(self, db_session):
        uuids = create_tasks_for_various_users()
        assert len(uuids) == 15

        first_user = User.get_by(username='jean_luc_picard')
        jean_luc_picard_tasks = Task.filter_by(user_uuids=[first_user.uuid],
                                               status=['pending', 'in_progress'],
                                               start_due_date= datetime.strptime('2025-01-02', '%Y-%m-%d'),
                                               end_due_date= datetime.strptime('2025-01-04 23:59:59',
                                                                               '%Y-%m-%d %H:%M:%S'))

        expected_uuids_values = {uuids[0], uuids[1]}
        uuid_values = {str(task.uuid) for task in jean_luc_picard_tasks}
        assert uuid_values == expected_uuids_values

        second_user = User.get_by(username='william_riker')
        third_user = User.get_by(username='deanna_troy')
        multi_user_tasks = Task.filter_by(user_uuids=[first_user.uuid, second_user.uuid, third_user.uuid],
                                          status=['completed'],
                                          start_due_date= datetime.strptime('2025-01-02 13:00',
                                                                            '%Y-%m-%d  %H:%M'),
                                          end_due_date= datetime.strptime('2025-01-06 10:20',
                                                                          '%Y-%m-%d %H:%M'))
        expected_uuids_values = {uuids[4], uuids[6], uuids[12]}
        uuid_values = {str(task.uuid) for task in multi_user_tasks}
        assert uuid_values == expected_uuids_values
