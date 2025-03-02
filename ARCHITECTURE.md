# DESCRIPTION

This a RESTful python flask API application for task management that uses PostgreSQL for persistance and Celery+RabbitMQ for background tasks.

It also leverages JWT for authentication (with refresh tokens).

I will start with the simplest architecture possible:

1) Data Layer (PostgreSQL)
2) API Layer (Flask)
3) Background Processing Layer (RabbitMQ with workers)

This architecture is simple and effective for a task management API with background processing.

If I have time to improve it, then it can be refactored with some concepts of clean/hexagonal architecture.

## Data Layer

This layer handles all data persistency.

I chose to use "Fat Models", so they contain all the business logic.

(TODO: revise this before sending) NOTE: I could just have used a flask library that provided an automatic restful wrapper on the models, without giving them this responsibility. But then this application would be much less interesting. ;)

### Database tables

```
user:
- uuid
- username
- email
- password_hash (will need `flask-bcrypt` python lib)
- created_at
- last_updated_at
- tasks (backref)

---

task:
- uuid
- title
- description
- status (created, in_progress, completed, archived, deleted)
- due_date
- created_at
- last_updated_at
- user_id (FK)
```

## API Layer (Flask)

This layer is responsible for collecting the user requests and directing them to the appropriate model(s) on the Data Layer. So, it contains no business logic.

The user authentication uses JWT.

## Background Processing Layer (RabbitMQ with workers)

TBD
