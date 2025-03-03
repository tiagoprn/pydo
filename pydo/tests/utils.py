from datetime import datetime, timedelta
from typing import List

from pydo.models import User, Task


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
