
# ToDo App

An application to create, list, update, and delete tasks



## Installation

Install and update using pip:

```
1. Clone the repository::

        git clone https://github.com/freddyB19/todo-app.git
        cd todo-app

2. Create and activate a virtual environment::

        python3 -m venv env
        source env/bin/activate

3. Install requirements::

        pip install -r requirements.txt

4. Run the application::
        
        python3 manage.py migrate
        python3 manage.py runserver
```
## Views

### Root URL 
```http
   /todo/
```
### CreateTaskFormView()
- _URL_: **/task/create/**

View to create tasks

### TasksListView()
- _URL_: **/task/list/**
- Pagination: 
  - param: ( page )
  - paginate_by: 3

View to see all tasks. With this you can perform filtered searches for tasks _(completed, uncompleted and all tasks)_

### DetailTaskDetailView()
- _URL_: **/task/{pk}/detail/**
- pk = task id

View to see the details of a task

### UpdateInfoTaskView()
- _URL_: **/task/{pk}/info/update/**
- pk = task id

View to see updating a task, when the operation is successful it redirects you to the task list view

### CompleteTaskView()
- _URL_: **/task/{pk}/status/update/**
- pk = task id

View to partially update a task. With this view you can mark a task as completed, when the operation is successful it redirects you to the task list view

### DeleteTaskView()
- _URL_: **/task/{pk}/delete/**
- pk = task id

View to delete a task, when the operation is successful it redirects you to the task list view


## API Reference

For API configurations, the following was done:

- There is a limit of 2000 requests to create a task per day

- There is a limit of 5000 requests to list all tasks per day
- CORS ALLOWED ORIGINS (localhost:8000)
- CSRF TRUSTED ORIGINS (localhost:8000)
- CORS DEFAULT METHODS = **ACTIVATED**
- CORS DEFAULT HEADERS = **ACTIVATED**


### Root URL 
```http
   /todo/api/v1/
```

#### POST create task

```http
  GET /task/create/
```
**Response::**
1. Valid:
- HTTP 201 Created
- Return the created task
- Pagination: 
  - params: (limit, offset)
  - default_limit: 5
  - max_limit: 10



#### Get all tasks

```http
  GET /tasks/
```


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `?is_complete=` | `bool` | **Optional**. To do filtered searches |

**Response::**
1. Valid:
- HTTP 200 OK
- Return a list of tasks
- Pagination: 
  - params: (limit, offset)
  - default_limit: 5
  - max_limit: 10



#### Get task

```http
  GET /task/${pk}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. Id of item to fetch |

**Response::**
1. Valid:
- HTTP 200 OK
- Return the detail of a task
2. Invalid
- HTTP 404 Not Found
```json
"error": {
        "message": "There is no task with this id"
   }
```

#### Update task

```http
  PUT /task/${pk}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. Id of item to fetch |

**Response::**
1. Valid:
- HTTP 200 OK
- Return the updated task
2. Invalid
- HTTP 404 Not Found
```json
"error": {
        "message": "There is no task with this id"
 }
```

#### Update Partial task

```http
  PATCH /task/${pk}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. Id of item to fetch |

**Response::**
1. Valid:
- HTTP 200 OK
- Return the updated task
2. Invalid
- HTTP 404 Not Found
```json
"error": {
        "message": "There is no task with this id"
 }
```

#### Delete task

```http
  DELETE /task/${pk}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. Id of item to fetch |

**Response::**
1. Valid:
- HTTP 204 No Content
2. Invalid
- HTTP 404 Not Found
```json
"error": {
        "message": "There is no task with this id"
 }
```


## Running Tests

The tests for the project are located in the ***tests folder***.

In it you can find the tests for:
- Models
- Views
- Forms

To run tests, run the following command:

### Test Models
```bash
  python3 manage.py test apps.task.tests.tests_models
```
### Test Forms
```bash
  python3 manage.py test apps.task.tests.tests_models
```
### Test Views
```bash
  python3 manage.py test apps.task.tests.tests_models
```
### API Tests

The API tests are located in the ***apiv1 folder***

Command:

```bash
  python3 manage.py test apps.task.apiv1
```

## Deployment

> [!IMPORTANT]
> It is recommended to make some configurations to run in production. Since this project does not meet all the requirements

For more information read the following documentations:

[Django](https://docs.djangoproject.com/en/5.0/)

[Django REST framework](https://www.django-rest-framework.org/).

[django-cors-headers](https://github.com/adamchainz/django-cors-headers).

