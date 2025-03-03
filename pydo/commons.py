import os
import re
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

from sqlalchemy.orm import Query
from sqlalchemy.dialects import postgresql


def get_query_raw_sql(query: Query) -> str:
    """
    Convert a SQLAlchemy query to a readable SQL string with parameters.

    Useful for debugging.
    """
    try:
        # Try with PostgreSQL dialect which handles UUIDs better
        raw_query = str(
            query.statement.compile(
                dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True}
            )
        )
    except Exception:
        # Fallback to parameters approach if literal binds fail
        compiled = query.statement.compile()
        params = compiled.params
        raw_query = f'{str(compiled)} [params: {params}]'

    raw_query = re.sub(r'\s+', ' ', raw_query).strip()
    return raw_query


def get_version_file_path() -> str:
    root_path = Path().absolute()
    file_path = os.path.join(str(root_path), 'VERSION')

    # needed to run the tests, since there it will be
    # on the pydo package directory,
    # not in the projects' root dir:
    if not os.path.exists(file_path):
        root_path = root_path.parent
        file_path = os.path.join(str(root_path), 'VERSION')

    return file_path


@lru_cache(maxsize=None)
def get_app_version():
    file_path = get_version_file_path()
    with open(file_path, 'r', encoding='utf-8') as version_file:
        return version_file.read().replace('\n', '')


def format_list_of_tasks(tasks: List['Task']) -> List[Dict]:  # noqa
    """
    Given tasks, iterate through each one and format it as a python dict.

    This is mainly intended to be used by the API.
    """
    # NOTE: imported here to avoid a circular dependency.
    #       Maybe I should move this as a static method
    #       of the Task model? Not sure, so will keep it here for now.
    from pydo.models import Task  # noqa

    formatted_tasks = []
    for task in tasks:
        formatted_task = {
            'uuid': str(task.uuid),
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'due_date': task.due_date.isoformat(),
            'created_at': task.created_at.isoformat(),
            'last_updated_at': task.last_updated_at.isoformat(),
            'user_uuid': task.user_uuid,
            'user_name': task.user.username,
        }
        formatted_tasks.append(formatted_task)
    return formatted_tasks


def paginate_query(resultset: List, page_number: int) -> Dict:
    """
    Simple implementation to paginate a list of records.
    """

    # NOTE: change this to be set on the app settings (+ env file)
    ITEMS_PER_PAGE = 5

    total_pages = (len(resultset) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # make sure the page number is valid
    if page_number < 1:
        page_number = 1
    elif page_number > total_pages and total_pages > 0:
        page_number = total_pages

    start_index = (page_number - 1) * ITEMS_PER_PAGE
    end_index = min(start_index + ITEMS_PER_PAGE, len(resultset))

    page_records = resultset[start_index:end_index]

    result = {
        'records': page_records,
        'total_pages': total_pages,
        'current_page': page_number,
        'has_next': page_number < total_pages,
        'has_prev': page_number > 1,
    }

    return result
