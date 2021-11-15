Environment: 
----------------

python 3.9.8

Flask 2.0.2

ORM: sqlalchemy

Web server: Nginx

Containerization tools: Docker

Testing Method: Unit testing

--------------------------------
Docker Command: docker-compose up --build

Test Command: docker exec -it flask python -m unittest

Todo Task
---------------------------------
List all task:
--------------
Method: GET

Endpoint_1: http://localhost/task/api/v1.0/tasks

Create a Task:
--------------
Method: POST

Endpoint_2: http://localhost/task/api/v1.0/tasks

Request:

Type:JSON

data: {"title": "Task 1","description":"hello testing"}

Get a task by id:
----------------
Method: GET

Endpoint_3: http://localhost/task/api/v1.0/tasks/1

Update a Task
-------------
Method: PUT

Endpoint_4: http://localhost/task/api/v1.0/tasks/1

Request:

Type:JSON

data: {"title": "Task 1","description":"test again", "done":True}

Delete a Task:
--------------
Method: Delete

Endpoint_4: http://localhost/task/api/v1.0/tasks/1

