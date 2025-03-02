## 2025-03-02

### DOING

- [-] API Layer
    - [-] Implement remaining endpoints:
        - [-] task
            - [ ] post
            - [ ] patch
            - [ ] delete
            - [ ] get
                - [ ] single
                - [ ] with filter
    - [ ] Manually test interacting with the API on swagger (make sure everything is working)
        - [ ] Update the docs with the link to access swagger API

### NEXT

- [ ] Background Tasks Layer
    - [ ] send an e-mail when a new task is created
        - [ ] create a `services` module to abstract the notification backend (start with e-mail)
            - [ ] Abstract class "Notification" with Abstract method "notify"
                - [ ] Derive an "E-mail notification" class from this one
    - [ ] ARCHITECTURE.md: Document how it will work
- [ ] tests: test the coverage report (`Makefile` command)
- [ ] populate the database with some tasks - using a `flask shell` script; add command to the Makefile
- [ ] implement rate limiting
- [ ] review ARCHITECTURE.md once more
- [ ] review the README.md once more
- [ ] Dockerize (update Dockerfile)
- [ ] pre-commit hook (install `pre-commit` through `uv` and put command on the `Makefile` to do that)

### DID

- [-] API Layer
    - [-] Implement remaining endpoints:
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
