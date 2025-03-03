import logging
from datetime import datetime, timedelta
from random import randint

import flask
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from pydo.commons import format_list_of_tasks
from pydo.exceptions import APIError
from pydo.models import User, Task
from pydo.settings import VERSION
from pydo.tasks import compute, generate_random_string

api_blueprint = Blueprint('api', __name__)

logger = logging.getLogger(__name__)


@api_blueprint.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error.payload)
    response.status_code = error.status_code
    return response


@api_blueprint.route('/compute', methods=['GET'])
def call_compute_task():
    """
    Put a compute task on the queue.

    Runs the compute function asynchronously,
    through sending a task to celery.

    The function called is actually a celery task, that must have
    a celery worker up listening to the queue so that it can be executed.
    ---
    tags:
      - Celery background task
    responses:
      200:
        description: message was put on the queue.
    """

    random_number = randint(1000, 9999)
    now_timestamp = datetime.now().isoformat()

    compute.apply_async(
        kwargs={'random_number': random_number, 'now_timestamp': now_timestamp}
    )

    return jsonify({'message': 'Successfully sent to queue.'})


@api_blueprint.route('/string', methods=['GET'])
def call_generate_random_string_task():
    """
    Put a generate random string task on the queue.

    Runs the generate random string function asynchronously,
    through sending a task to celery.

    The function called is actually a celery task, that must have
    a celery worker up listening to the queue so that it can be executed.
    ---
    tags:
      - Celery background task
    responses:
      200:
        description: message was put on the queue.
    """

    generate_random_string.apply_async()

    return jsonify({'message': 'Successfully sent to queue.'})


@api_blueprint.route('/health-check/readiness', methods=['GET'])
def readiness():
    """
    Used by k8s, to know when a container is ready.

    The kubelet uses readiness probes to know when a container
    is ready to start accepting traffic.

    A Pod is considered ready when all of its Containers are ready.
    One use of this signal is to control which Pods are used as
    backends for Services.
    When a Pod is not ready, it is removed from Service load balancers.
    This will run ONLY ONCE.
    ---
    tags:
      - Healthcheck
    responses:
      200:
        description: show the app as ready, with its app version and type.
    """
    flask_version = flask.__version__
    app_type = f'flask-framework {flask_version}'
    response_dict = {
        'ready': 'OK',
        'app_version': VERSION,
        'app_type': f'{app_type}',
    }

    return jsonify(response_dict)


@api_blueprint.route('/health-check/liveness', methods=['GET'])
def liveness():
    """
    Used by k8s, to know if a Container is live.

    The kubelet uses liveness probes to know when to restart a Container. For
    example, liveness probes could catch a deadlock, where an application is
    running, but unable to make progress. Restarting a Container in such a
    state can help to make the application more available despite bugs. This
    will run ON REGULAR INTERVALS.
    ---
    tags:
      - Healthcheck
    responses:
      200:
        description: show the app as live, with its version
                     and the current timestamp.
    """
    timestamp = datetime.now().isoformat()
    response_dict = {
        'live': 'OK',
        'version': VERSION,
        'timestamp': timestamp,
    }
    return jsonify(response_dict)


@api_blueprint.route('/welcome/<person>', methods=['GET'])
def welcome(person: str):
    """
    Returns a welcome message with custom text.
    ---
    tags:
      - Example
    parameters:
      - name: person
        in: path
        type: string
        required: true
    responses:
      200:
        description: the welcome message.
    """
    response_dict = {'message': f'Hello, {person}!'}
    return jsonify(response_dict)


@api_blueprint.route("/login", methods=["POST"])
def login():
    """
    Login
    ---
    tags:
      - JWT Auth
    parameters:
      - name: email
        type: string
        required: true
      - name: password
        type: string
        required: true
    responses:
      200:
        description: JWT temporary access token & JWT long-live refresh token
    """
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = User.get_by(email=email)
    is_valid_password = user.check_password(password=password)

    if user and is_valid_password:
        # temporary access token:
        access_token = create_access_token(identity=str(user.uuid), expires_delta=timedelta(hours=1))

        # long-live refresh token:
        refresh_token = create_refresh_token(identity=str(user.uuid))

        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200

    return jsonify({"msg": "Invalid credentials"}), 401


@api_blueprint.route("/token/new", methods=["POST"])
@jwt_required(refresh=True)  # with this param, requires the refresh token (long-live one)
def token_refresh():
    """
    Get a new JWT temporary access token (expires in 1 hour)
    ---
    tags:
      - JWT Auth
    responses:
      200:
        description: JWT temporary access token
    """
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": new_access_token}), 200


@api_blueprint.route("/user", methods=["POST"])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: username
        type: string
        required: true
      - name: email
        type: string
        required: true
      - name: password
        type: string
        required: true
    responses:
      201:
        description: created user data.
    """
    data = request.get_json()

    new_user = User().register(**data)

    return jsonify({"uuid": str(new_user.uuid)}), 201


@api_blueprint.route("/user", methods=["GET"])
@jwt_required()  # with no params, requires the access token (temporary one)
def get_user():
    """
    Get user info
    ---
    tags:
      - Users
    responses:
      200:
        description: user info
    """
    user_uuid = get_jwt_identity()

    user = User.get_by(uuid=user_uuid)
    return jsonify({"uuid": str(user.uuid), "username": user.username, "email": user.email}), 200


@api_blueprint.route("/user", methods=["PATCH"])
@jwt_required()
def update_user():
    """
    Update user info
    ---
    tags:
      - Users
    parameters:
      - name: email
        type: string
        required: false
      - name: password
        type: string
        required: false
    responses:
      200:
        description: updated user info
    """
    user_uuid = get_jwt_identity()

    data = request.get_json()
    user = User.get_by(uuid=user_uuid)

    email = data.get('email')
    password = data.get('password')
    user.update(email=email, password=password)

    password_value = 'SUCCESSFULLY CHANGED' if password else 'NOT CHANGED'
    return jsonify({"uuid": str(user.uuid), "email": user.email, "password": password_value}), 200


@api_blueprint.route("/task", methods=["POST"])
@jwt_required()
def create_task():
    """
    Create task
    ---
    tags:
      - Tasks
    parameters:
      - name: title
        type: string
        required: true
      - name: description
        type: string
        required: true
      - name: status
        type: string (pending, in_progress, completed)
        required: false
      - name: due_date
        type: string (YYYY-MM-DD HH:MM)
        required: false
    responses:
      200:
        description: task info
    """
    user_uuid = get_jwt_identity()
    user = User.get_by(uuid=user_uuid)

    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    due_date = data.get('due_date')

    new_data = {
        'user_uuid': user_uuid,
        'title': title,
        'description': description,
        'status': status if status else 'pending',
    }
    if due_date:
        new_data['due_date'] = datetime.strptime(due_date, '%Y-%m-%d %H:%M')
        # TODO: valid date and date >= datetime.utcnow()

    # TODO: validate status

    created_task_instance = Task().create(**new_data)

    created_task_data = {
        'uuid': created_task_instance.uuid,
        'title': created_task_instance.title,
        'description': created_task_instance.description,
        'status': created_task_instance.status,
        'due_date': created_task_instance.due_date.isoformat(),
        'created_at': created_task_instance.created_at.isoformat(),
        'last_updated_at': created_task_instance.last_updated_at.isoformat()
    }
    return jsonify(created_task_data), 201


@api_blueprint.route("/task", methods=["PATCH"])
@jwt_required()
def update_task():
    """
    Update task
    ---
    tags:
      - Tasks
    parameters:
      - name: uuid
        type: string
        required: true
      - name: title
        type: string
        required: true
      - name: description
        type: string
        required: true
      - name: status
        type: string (pending, in_progress, completed)
        required: false
      - name: due_date
        type: string (YYYY-MM-DD HH:MM)
        required: false
    responses:
      200:
        description: task info
    """
    user_uuid = get_jwt_identity()
    user = User.get_by(uuid=user_uuid)

    data = request.get_json()

    task_uuid = data.get('uuid')
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    due_date = data.get('due_date')

    updated_data = {
        'title': title,
        'description': description,
        'status': status if status else 'pending',
    }
    if due_date:
        updated_data['due_date'] = datetime.strptime(due_date, '%Y-%m-%d %H:%M')
        # TODO: valid date and date >= datetime.utcnow()

    # TODO: validate status

    task_instance = Task().filter_by(uuids=[task_uuid])[0]
    task_instance.update(**updated_data)

    updated_task_data = {
        'uuid': task_instance.uuid,
        'title': task_instance.title,
        'description': task_instance.description,
        'status': task_instance.status,
        'due_date': task_instance.due_date.isoformat(),
        'created_at': task_instance.created_at.isoformat(),
        'last_updated_at': task_instance.last_updated_at.isoformat()
    }
    return jsonify(updated_task_data), 200

@api_blueprint.route("/task", methods=["DELETE"])
@jwt_required()
def delete_task():
    """
    Delete task
    ---
    tags:
      - Tasks
    parameters:
      - name: uuid
        type: string
        required: true
    responses:
      204:
        description: successfully deleted
      400:
        description: not deleted (non-existing or error during deletion)
    """
    user_uuid = get_jwt_identity()
    user = User.get_by(uuid=user_uuid)

    data = request.get_json()
    task_uuid = data.get('uuid')

    deleted = Task.delete(user_uuid=user_uuid, uuid=task_uuid)

    if deleted:
        return '', 204

    return jsonify({'message': 'could not delete task (non-existing or error during deletion)'}), 400

@api_blueprint.route("/task", methods=["GET"])
@jwt_required()
def get_one_task():
    """
    Get one task
    ---
    tags:
      - Tasks
    parameters:
      - name: uuid
        type: string
        required: true
    responses:
      200:
        description: success
    """
    user_uuid = get_jwt_identity()
    user = User.get_by(uuid=user_uuid)

    data = request.get_json()
    task_uuid = data.get('uuid')

    task_instance = Task().filter_by(uuids=[task_uuid], user_uuids=[user_uuid])[0]

    task_data = {
        'uuid': task_instance.uuid,
        'title': task_instance.title,
        'description': task_instance.description,
        'status': task_instance.status,
        'due_date': task_instance.due_date.isoformat(),
        'created_at': task_instance.created_at.isoformat(),
        'last_updated_at': task_instance.last_updated_at.isoformat()
    }
    return jsonify(task_data), 200


@api_blueprint.route("/tasks", methods=["GET"])
@jwt_required()
def get_many_tasks():
    """
    Get many tasks

    ---
    tags:
      - Tasks
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            user_uuids:
              type: array
              items:
                type: string
              description: List of user UUIDs to filter tasks by
            uuids:
              type: array
              items:
                type: string
              description: List of task UUIDs to retrieve
            status:
              type: array
              items:
                type: string
                enum: [pending, completed, in_progress]
              description: Filter tasks by status
            start_due_date:
              type: string
              format: date
              description: Filter tasks with due date on or after this date (YYYY-MM-DD HH:MM)
            end_due_date:
              type: string
              format: date
              description: Filter tasks with due date on or before this date (YYYY-MM-DD HH:MM)
          example:
            user_uuids: ["U123ABC", "U456DEF"]
            uuids: ["T78F", "G32P"]
            status: ["pending", "completed"]
            start_due_date: "2025-01-05 00:00"
            end_due_date: "2025-01-15 23:59"
    responses:
      200:
        description: success
    """
    user_uuid = get_jwt_identity()
    user = User.get_by(uuid=user_uuid)

    data = request.get_json()

    task_uuids = data.get('uuids', [])
    user_uuids = data.get('user_uuids', [])
    status = data.get('status', [])
    start_due_date_str = data.get('start_due_date', None)
    end_due_date_str = data.get('end_due_date', None)

    start_due_date = datetime.strptime(start_due_date_str, '%Y-%m-%d %H:%M') if start_due_date_str else None
    end_due_date = datetime.strptime(end_due_date_str, '%Y-%m-%d %H:%M') if end_due_date_str else None

    # TODO: Use limit...offset on the query to paginate
    filtered_tasks_instances = Task.filter_by(user_uuids=user_uuids, uuids=task_uuids, status=status,
                                              start_due_date=start_due_date, end_due_date=end_due_date)

    filtered_tasks = format_list_of_tasks(tasks=filtered_tasks_instances)

    return jsonify(filtered_tasks), 200
