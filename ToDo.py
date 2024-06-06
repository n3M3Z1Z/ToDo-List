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
from flask import Flask, jsonify, request
import api_beispieldaten as ts
  
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

# Funktion um zu checken, ob auch wirklich ein Wert übergeben wurde
def is_valid_value(value):
    return value not in (None, '', [], {}, ())
"""
    # set endpoint to retrieve all tasks
    
    retrieve all tasks
    
    returns:
    JSON: a list of all tasks.
"""

# Set endpoint to retrieve all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    if not tasks:
        return jsonify({"message": "Es gibt keine Tasks"}), 404
    return jsonify(message="Look at your mess, way to many open tasks, get them done!", tasks=tasks)

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
        return jsonify({"Fehler": "Nope, site dosen't exit - search elsewhere"}), 404

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
    if not request.json:
        return jsonify({"Fehler": "Request muss im JSON-Format sein"}), 400 
    if 'title' not in request.json or 'description' not in request.json:
        return jsonify({"Fehler": "Es müssen sowohl der title, wie auch die description gesetzt sein. Sollstest du eigent wissen"}), 400
    
    try:
        new_task = {
            "id": tasks[-1]["id"] + 1,
            "title": request.json["title"],
            "description": request.json["description"],
            "status": request.json.get("status", "pending"), # Default value is pending
            "priority": request.json.get("priority", "niedrig"),
            "due_date": request.json.get("due_date", None)
        }
        tasks.append(new_task)
        return jsonify(new_task), 201
    
    except Exception as e:
        return jsonify({"Fehler": str(e)}), 400

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
    # schaue ob der Task existiert
    if task is None:
        return jsonify({"Fehler": "Nope, no such task, running ransomware instead"}), 404
    try:
        # nun überprüfe, ob irgendein Key angegeben ist und ersetze ihn, sollte der key auch einen Wert enthalten
        if any(field in request.json for field in ['title', 'status', 'description', 'priority', 'due_date']):
            task["title"] = request.json.get("title", task["title"]) if is_valid_value(request.json.get("title")) else task["title"]
            task["status"] = request.json.get("status", task["status"]) if is_valid_value(request.json.get("status")) else task["status"]
            task["description"] = request.json.get("description", task["description"]) if is_valid_value(request.json.get("description")) else task["description"]
            task["priority"] = request.json.get("priority", task["priority"]) if is_valid_value(request.json.get("priority")) else task["priority"]
            task["due_date"] = request.json.get("due_date", task["due_date"])if is_valid_value(request.json.get("due_date")) else task["due_date"]
            return jsonify(message="know what? find the error yourself! Good Luck!", task=task)
        
    except Exception as e:
        return jsonify({"Zipfelklatscher": str(e)}), 400

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
        return jsonify({"Fehler": "Nope, der Task existiert nicht - Entferne System32"}), 404
    tasks.remove(task)
    return jsonify(message="System32 deleted", task=task)

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
        return jsonify({"Fehler": "Nope, der Task existiert nicht, oder ist zu schüchtern um angezeigt zu werden"}), 404
    task["status"] = "completed"
    return jsonify(Message="you marked it you do it! I'll check it!", task=task)

"""
    # set endpoint to retrieve all completed tasks
    
    retruns:
    JSON: a list of all completed tasks.
"""

# Set endpoint to retrieve all completed tasks
@app.route('/tasks/completed', methods=['GET'])
def get_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    if not completed_tasks:
        return jsonify({"message": "Es gibt keine Tasks in completed - habe auch nichts anderes von dir erwartet :P"}), 404
    return jsonify(message="Good Boy!", completed_tasks=completed_tasks)

"""
    # set endpoint to retieve all pending tasks
    
    returns:
    JSON: a list of all pending tasks.
"""

# Set endpoint to retrieve all pending tasks
@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    if not pending_tasks:
        return jsonify({"message": "Es gibt keine Tasks in pending - war ja auch irgendwie klar"}), 404
    return jsonify(message="Do or do not - there is no pending!", pending_tasks=pending_tasks)

"""
    # set endpoint to retrieve tasks by priority level
    
    parameters:
    level (string): Priority level of the task.
    
    returns:
    JSON: a list of tasks with specified priority level.
"""

# Set endpoint to retrieve tasks by priority level
@app.route('/tasks/priority/<string:level>', methods=['GET'])
def get_tasks_by_proirity_level(level):
    level_list = ["hoch", "niedrig", "mittel"]
    if level in level_list:
        priority_tasks = [task for task in tasks if task["priority"] == level]
        return jsonify(message="have fun", priority_tasks=priority_tasks)
    else:
        return jsonify({"error": "Dieses Prioritäts-Level existiert nicht"}), 400

"""
    # set endpoint to delete all completed tasks
    
    retrurns:
    JSON: a list of deleted completed tasks.
"""

# Set endpoint to delete all completed tasks
@app.route('/tasks/completed', methods=['DELETE'])
def delete_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    if not completed_tasks:
        return jsonify({"message": "Es gibt keine Tasks in completed - war zu erwarten"}), 404
    for task in completed_tasks:
        tasks.remove(task)
    return jsonify(message="ooh someone want to tidy up the mess he made. Good Boy!", completed_tasks=completed_tasks)

"""
    # set endpoint to delete all pending tasks
    
    retrurns:
    JSON: a list of deleted pending tasks.
"""

# Set endpoint to delete all pending tasks
@app.route('/tasks/pending', methods=['DELETE'])
def delete_pending_tasks():
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    # wenn keine Tasks in pending vorliegen
    if not pending_tasks:
        return jsonify({"message": "Es gibt keine Tasks in pending - wundert mich nicht"}), 404
    for task in pending_tasks:
        tasks.remove(task)
    return jsonify(message="Bye Bye files Bye Bye!", pending_tasks=pending_tasks)

# Set 'main' function to run the app
if __name__ == "__main__":
    app.run(debug=True)