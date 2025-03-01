## 2025-03-01

### DOING

- [-] Create the README with the cookiecutter instructions to develop on the project
- [-] Data Layer
    - [-] create the database models

### NEXT

- [ ] Check how to integrate JWT authentication
    - [ ] Which library to use?
    - [ ] ARCHITECTURE.md: Document how it will work
- [ ] API Layer
    - [ ] Maybe do not use any library to make the API RESTful, because this will lock the app into a library.
          (maybe create a `use_cases` module to do the operations on the models)
    - [ ] ARCHITECTURE.md: Document how it will work
- [ ] Background Tasks Layer
    - [ ] send an e-mail when a new task is created
        - [ ] create a `services` module to abstract the notification backend (start with e-mail)
            - [ ] Abstract class "Notification" with Abstract method "notify"
                - [ ] Derive an "E-mail notification" class from this one
    - [ ] ARCHITECTURE.md: Document how it will work
- [ ] seed the database with some tasks
- [ ] Dockerize (update Dockerfile)
- [ ] revise the README.md once more
- [ ] use "git-secret": migrate `.env.JWT_SECRET_KEY` to there
- [ ] deploy to a VPS ? (if I have time)
- [ ] adhere to Clean Architecture principles, including separation of concerns and independence of components.

### DID

- [-] Data Layer
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
