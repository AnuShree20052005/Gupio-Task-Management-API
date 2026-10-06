# Gupio Task Management API

A RESTful Task Management API built using Flask, Flask-SQLAlchemy and PostgreSQL/SQLite.

## Features

- Create a task
- Get all tasks
- Get a task by ID
- Update a task
- Delete a task
- Search tasks by title
- Filter tasks by status
- Filter tasks by priority
- Input validation
- Missing-record handling
- JSON responses
- PostgreSQL support through `DATABASE_URL`
- SQLite fallback for local development
- CORS support
- Gunicorn deployment support

## Task fields

- `id`
- `title`
- `description`
- `status`: `pending`, `in_progress`, `completed`
- `priority`: `low`, `medium`, `high`
- `due_date`

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health check |
| POST | `/tasks` | Create task |
| GET | `/tasks` | List tasks |
| GET | `/tasks/<id>` | Get task by ID |
| PUT | `/tasks/<id>` | Update task |
| DELETE | `/tasks/<id>` | Delete task |

### Search and filters

```text
GET /tasks?search=Flask
GET /tasks?status=in_progress
GET /tasks?priority=high
```

Filters can also be combined:

```text
GET /tasks?status=pending&priority=high
```

## Local setup - Windows PowerShell

Open PowerShell inside the `task` folder.

### 1. Create virtual environment

```powershell
python -m venv venv
```

### 2. Activate it

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 3. Install packages

```powershell
pip install -r requirements.txt
```

### 4. Configure environment

Create a file named `.env`.

For local SQLite testing:

```text
DATABASE_URL=sqlite:///tasks.db
```

For Neon PostgreSQL, use your private Neon connection string:

```text
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST/DATABASE?sslmode=require
```

The application automatically changes the PostgreSQL URL to use the `psycopg2` driver.

### 5. Run

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

## Example POST request

POST `/tasks`

```json
{
  "title": "Complete Gupio Backend Assignment",
  "description": "Build and test the Task Management REST API",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-10-10"
}
```

Expected status:

```text
201 Created
```

## Example response

```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete Gupio Backend Assignment",
    "description": "Build and test the Task Management REST API",
    "status": "pending",
    "priority": "high",
    "due_date": "2026-10-10"
  }
}
```

## Deployment

For a platform such as Render:

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn app:app
```

Add this environment variable in the deployment dashboard:

```text
DATABASE_URL=<your private Neon PostgreSQL connection string>
```

Never commit `.env` or database credentials to GitHub.

## Error examples

Missing title:

```json
{
  "error": "Title is required"
}
```

Missing task:

```json
{
  "error": "Task not found"
}
```

## Verification checklist

- Create task
- Retrieve all tasks
- Retrieve task by ID
- Update task
- Delete task
- Search by title
- Filter by status
- Filter by priority
- Test invalid input
- Test missing record

## Author

AnuShree B S
