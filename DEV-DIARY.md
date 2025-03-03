## 2025-03-03

### DOING

- [ ] review ARCHITECTURE.md once more
    - [ ] Background Tasks Layer
        - [ ] Document how it works

### DID

- [x] apply ruff; re-run the tests
- [x] review the README.md once more
- [x] tests: test the coverage report (`Makefile` command)
- [-] API Layer
    - [x] Implement remaining endpoints:
        - [x] task
            - [x] post
                - [x] A user_uuid can create a task for other user_uuid (add a test).
                      If the user_uuid is not informed, create for himself.
            - [x] get
                - [x] Explain the decision to not use a serializer to return tasks, and the "manual pagination" also
                - [x] all
                    - [x] implement pagination on the API layer (customizable on .env; 3 per page for testing purposes)
                    - [x] without filter
                    - [x] with filter

## 2025-03-02

### DID

- [-] API Layer
    - [x] Manually test interacting with the API on swagger (make sure everything is working)
        - [A] Update the docs with the link to access swagger API
        - [A] swagger is not allowing interacting with the API, generate and provide a postman collection
        - [x] Provide a postman collection.
    - [x] Implement remaining endpoints:
        - [x] task
            - [x] get
                - [x] single
            - [x] post
            - [x] patch
            - [x] delete
        - [x] user
            - [x] patch
    - [x] Implement the JWT endpoints
    - [x] Add `flask-jwt-extended` to requirements and update the `uv venv`
    - [x] Check how to integrate JWT authentication
        - [x] Which library to use?
        - [x] ARCHITECTURE.md: Document how it will work
- [x] Data Layer
    - [x] database models
        - [x] Task model methods
            - [x] create
            - [x] update
            - [x] filter_by

## 2025-03-01

### DID

- [-] Data Layer
    - [-] database models
        - [-] create with tests:
            - [x] User model methods
        - [x] cli to access the database:
            - [x] install pgcli (using `uv tool` if it is a python app)
            - [x] configure pgcli
            - [x] run pgcli and inspect the database
            - [x] Makefile: add command to run pgcli
        - [x] create (details: `ARCHITECTURE.md`)
        - [x] on `Task.status`, make the choices deterministic
        - [x] delete the migrations generated from the cookiecutter
        - [x] delete the containers generated from the cookiecutter
        - [x] start new containers
        - [x] create the migration
        - [x] run the migration
        - [x] run dev webserver
        - [x] run dev worker
    - [x] setup `bcrypt` as an app extension
    - [x] add bcrypt to requirements.in to allow hashing
        - [x] cleanup the previous requirements.in (has pylint and black which I do not use on this solution)
        - [x] re-generate the requirements.txt taking into consideration the cleaned up requirements.in
        - [x] create a new .venv, activate it and run the test suite to make sure all is great.
    - [x] design the database schema for storing tasks and users.
- [x] Define the application architecture.
- [x] Follow the instructions from the README to validate the project is on a functional state at the beginning
- [x] Initialize the project with my cookiecutter <https://github.com/tiagoprn/celery-db-flask-cookiecutter> -- under tmp/
- [x] Create the DEV-DIARY and the gitignore
