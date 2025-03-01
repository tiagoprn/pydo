from pydo.factory import create_app

app = create_app()

# Ensure tasks are registered
from pydo import tasks  # noqa
