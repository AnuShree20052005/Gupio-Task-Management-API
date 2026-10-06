import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from models import db, Task

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
# Uses PostgreSQL when DATABASE_URL is provided.
# Falls back to local SQLite for easy local development.
database_url = os.getenv("DATABASE_URL", "sqlite:///tasks.db")

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://", "postgresql+psycopg2://", 1
    )
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://", "postgresql+psycopg2://", 1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Gupio Task Management API is running!",
        "version": "1.0"
    }), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title is required"
        }), 400

    status = data.get("status", "pending")
    priority = data.get("priority", "medium")

    allowed_statuses = ["pending", "in_progress", "completed"]
    allowed_priorities = ["low", "medium", "high"]

    if status not in allowed_statuses:
        return jsonify({
            "error": "Invalid status. Use pending, in_progress or completed"
        }), 400

    if priority not in allowed_priorities:
        return jsonify({
            "error": "Invalid priority. Use low, medium or high"
        }), 400

    task = Task(
        title=title.strip(),
        description=data.get("description"),
        status=status,
        priority=priority,
        due_date=data.get("due_date")
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully",
        "task": task.to_dict()
    }), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    query = Task.query

    search = request.args.get("search")
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    status = request.args.get("status")
    if status:
        query = query.filter(Task.status == status)

    priority = request.args.get("priority")
    if priority:
        query = query.filter(Task.priority == priority)

    tasks = query.all()

    return jsonify({
        "count": len(tasks),
        "tasks": [task.to_dict() for task in tasks]
    }), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "task": task.to_dict()
    }), 200


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify({
                "error": "Title cannot be empty"
            }), 400
        task.title = data["title"].strip()

    if "description" in data:
        task.description = data["description"]

    if "status" in data:
        allowed_statuses = ["pending", "in_progress", "completed"]
        if data["status"] not in allowed_statuses:
            return jsonify({
                "error": "Invalid status. Use pending, in_progress or completed"
            }), 400
        task.status = data["status"]

    if "priority" in data:
        allowed_priorities = ["low", "medium", "high"]
        if data["priority"] not in allowed_priorities:
            return jsonify({
                "error": "Invalid priority. Use low, medium or high"
            }), 400
        task.priority = data["priority"]

    if "due_date" in data:
        task.due_date = data["due_date"]

    db.session.commit()

    return jsonify({
        "message": "Task updated successfully",
        "task": task.to_dict()
    }), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
