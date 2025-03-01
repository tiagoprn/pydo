## 2025-03-01

### DOING

- [-] Create the README with the cookiecutter instructions to develop on the project
- [-] Data Layer
    - [x] design the database schema for storing tasks and users.
    - [ ] add bcrypt to requirements.in to allow hashing/encryption
        - [ ] cleanup the previous requirements.in (has pylint and black which I do not use on this solution)
        - [ ] re-generate the requirements.txt taking into consideration the cleaned up requirements.in
        - [ ] create a new .venv, activate it and run the test suite to make sure all is great.
    - [ ] create the database models

- [ ] Check how to integrate JWT authentication
    - [ ] Which library to use?
    - [ ] ARCHITECTURE.md: Document how it will work

### NEXT

- [ ] Challenges (investigate how I can implement the following)
    - [ ] API Layer
        - [ ] Check if there is the need to use a specific package to make the models RESTful (check the requirements if it is not already there)
- [ ] seed the database with some tasks
- [ ] revise the README.md once more
- [ ] adhere to Clean Architecture principles, including separation of concerns and independence of components.

### DID

- [x] Define the application architecture.
- [x] Follow the instructions from the README to validate the project is on a functional state at the beginning
- [x] Initialize the project with my cookiecutter <https://github.com/tiagoprn/celery-db-flask-cookiecutter> -- under tmp/
- [x] Create the DEV-DIARY and the gitignore
