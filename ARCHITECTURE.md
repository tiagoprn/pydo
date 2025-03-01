# DESCRIPTION

This a RESTful python flask API application for task management that uses PostgreSQL for persistance and Celery+RabbitMQ for background tasks.

It also leverages JWT for authentication (with refresh tokens).

I will start with the simplest architecture possible:

1) API Layer (Flask)
2) Data Layer (PostgreSQL)
3) Background Processing Layer (RabbitMQ with workers)

This architecture is simple and effective for a task management API with background processing.

If I have time to improve it, then it can be refactored with some concepts of clean/hexagonal architecture.
