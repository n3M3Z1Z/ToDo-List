"""
This script implements a simple ToDo list API using Flask.
This API allows users to:
    - Create, Update, Delete, mark tasks as completed, filter or delete tasks by priority & status

Each task has the following structure:
    - id (integer): Unique identifier of the task
    - title (string): Title of the task
    - description (string): Description of the task
    - status (string): Status of the task
    - priority (integer): Priority of the task
    - due_date (string): Due date of the task  
"""

# Import necessary modules, files & libraries
import os
from flask import Flask, jsonify, request, abort
import tasks_templet as ts
  
# Define the API overall function 
app = Flask(__name__)

# Import 'tasks' from 'tasks_templet.py'
tasks = ts.tasks

"""
    # set endpoint to retrieve task by id
    
    parameters:
    task_id (int): Unique identifier of the task.
    
    returns:
    dict: task with specified id
"""

# Utility function to find task by id
def task_by_id(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

"""
    # set endpoint to retrieve all tasks
    
    retrieve all tasks
    
    returns:
    JSON: a list of all tasks.
"""

# Set endpoint to retrieve all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

"""
    # set endpoint to retrieve task by id
    
    parameters:
    task_id (int): Unique identifier of the task.
    
    returns:
    dict: task with given id
"""

# Set endpoint to retrieve a task by id
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_by_id(task_id)
    if task:
        return jsonify(task)
    else:
        abort(404)

"""
    # set endpoint to create a new task
    
    request JSON body:
    - title (string): Title of the task.
    - description (string): Description of the task.
    - priority (integer): Priority of the task.
    - due_date (string): Due date of the task.
"""

# Set endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(400)
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": request.json["title"],
        "description": request.json["description"],
        "status": request.json.get("status", "pending"),
        "priority": request.json.get("priority", 0),
        "due_date": request.json.get("due_date", "")
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

"""
    # set endpoint to update a specific task
    
    parameters: 
    id (int): Unique identifier of the task.
    
    returns:
    JSON: updated task
"""

# Set endpoint to update a specific task by its unique id
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = task_by_id(task_id)
    if task is None:
        abort(404)
    if not request.json:
        abort(400)
    task["title"] = request.json.get("title", task["title"])
    task["status"] = request.json.get("status", task["status"])
    task["description"] = request.json.get("description", task["description"])
    task["priority"] = request.json.get("priority", task["priority"])
    task["due_date"] = request.json.get("due_date", task["due_date"])
    return jsonify(task)

"""
    # set endpoint to delete tasks
    
    parameters: 
    id (int): Unique identifier of the task.
    
    returns:
    JSON: deleted task
"""

# Set endpoint to delete task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = task_by_id(task_id)
    if task is None:
        abort(404)
    tasks.remove(task)
    return jsonify(task)

"""
    # set endpont to mark a specific task as deleted
    
    parameters: 
    id (int): Unique identifier of the task.
    
    returns:
    JSON: deleted task
"""

# Set endpoint to mark a specific task
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = task_by_id(task_id)
    if task is None:
        abort(404)
    task["status"] = "completed"
    return jsonify(task)

"""
    # set endpoint to retrieve all completed tasks
    
    retruns:
    JSON: a list of all completed tasks.
"""

# Set endpoint to retrieve all completed tasks
@app.route('/tasks/completed', methods=['GET'])
def get_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    return jsonify(completed_tasks)

"""
    # set endpoint to retieve all pending tasks
    
    returns:
    JSON: a list of all pending tasks.
"""

# Set endpoint to retrieve all pending tasks
@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    return jsonify(pending_tasks)

"""
    # set endpoint to retrieve tasks by priority level
    
    parameters:
    level (string): Priority level of the task.
    
    returns:
    JSON: a list of tasks with specified priority level.
"""

# Set endpoint to retrieve tasks by priority level
@app.route('/tasks/priority/<string:level>', methods=['GET'])
def get_tasks_by_priority_level(level):
    filtered_tasks = [task for task in tasks if task["priority"] == level]
    return jsonify(filtered_tasks)

"""
    # set endpoint to delete all completed tasks
    
    retrurns:
    JSON: a list of deleted completed tasks.
"""

# Set endpoint to delete all completed tasks
@app.route('/tasks/completed', methods=['DELETE'])
def delete_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    for task in completed_tasks:
        tasks.remove(task)
    return jsonify(completed_tasks)

"""
    # set endpoint to delete all pending tasks
    
    retrurns:
    JSON: a list of deleted pending tasks.
"""

# Set endpoint to delete all pending tasks
@app.route('/tasks/pending', methods=['DELETE'])
def delete_pending_tasks():
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    for task in pending_tasks:
        tasks.remove(task)
    return jsonify(pending_tasks)

# Set 'main' function to run the app
if __name__ == "__main__":
    app.run(debug=True)