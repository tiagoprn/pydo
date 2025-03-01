## 2025-03-01

### DOING

- [-] Create the README with the cookiecutter instructions to develop on the project
- [-] Data Layer
    - [ ] create the database models
- [ ] Check how to integrate JWT authentication
    - [ ] Which library to use?
    - [ ] ARCHITECTURE.md: Document how it will work
- [ ] API Layer
- [ ] Background Tasks Layer
    - [ ] send an e-mail when a new task is created

### NEXT

- [ ] Challenges (investigate how I can implement the following)
    - [ ] API Layer
        - [ ] Check if there is the need to use a specific package to make the models RESTful (check the requirements if it is not already there)
- [ ] seed the database with some tasks
- [ ] Dockerize (update Dockerfile)
- [ ] revise the README.md once more
- [ ] deploy to a VPS ? (if I have time)
- [ ] adhere to Clean Architecture principles, including separation of concerns and independence of components.

### DID

- [-] Data Layer
    - [x] add bcrypt to requirements.in to allow hashing/encryption
        - [x] cleanup the previous requirements.in (has pylint and black which I do not use on this solution)
        - [x] re-generate the requirements.txt taking into consideration the cleaned up requirements.in
        - [x] create a new .venv, activate it and run the test suite to make sure all is great.
    - [x] design the database schema for storing tasks and users.
- [x] Define the application architecture.
- [x] Follow the instructions from the README to validate the project is on a functional state at the beginning
- [x] Initialize the project with my cookiecutter <https://github.com/tiagoprn/celery-db-flask-cookiecutter> -- under tmp/
- [x] Create the DEV-DIARY and the gitignore
