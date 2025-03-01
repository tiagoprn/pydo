## 2025-03-01

### DOING

- [-] Create the README with the cookiecutter instructions to develop on the project
- [-] Data Layer
    - [-] database models
        - [-] create and run tests:
            - [ ] Task model:
                - [ ] status values (valid, invalid)
        - [ ] create a new User using flask shell (to validate the app factory and the extensions)

### NEXT

- [ ] Makefile: add command to run `flask shell` on the project
- [ ] tests: test the coverage report (`Makefile` command)
- [ ] API Layer
    - [ ] Check how to integrate JWT authentication
        - [ ] Which library to use?
        - [ ] ARCHITECTURE.md: Document how it will work
    - [ ] Maybe do not use any library to make the API RESTful, because this will lock the app into a library.
          (maybe create a `use_cases` module to do the operations on the models)
    - [ ] implement rate limiting
    - [ ] ARCHITECTURE.md: Document how it will work
- [ ] Background Tasks Layer
    - [ ] send an e-mail when a new task is created
        - [ ] create a `services` module to abstract the notification backend (start with e-mail)
            - [ ] Abstract class "Notification" with Abstract method "notify"
                - [ ] Derive an "E-mail notification" class from this one
    - [ ] ARCHITECTURE.md: Document how it will work
- [ ] populate the database with some tasks - using a `flask shell` script; add command to the Makefile
- [ ] Dockerize (update Dockerfile)
- [ ] revise the README.md once more
- [ ] use "git-secret": migrate `.env.JWT_SECRET_KEY` to there
- [ ] pre-commit hook (install `pre-commit` through `uv` and put command on the `Makefile` to do that)
- [ ] CI pipeline (github actions):
    - [ ] ruff lint/format check
    - [ ] tests (with coverage report)
- [ ] deploy to a VPS ? (if I have time)
- [ ] adhere to Clean Architecture principles, including separation of concerns and independence of components.

### DID

- [-] Data Layer
    - [-] database models
        - [-] create and run tests:
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
