"""
    this script implements a simple ToDo list API using Flask.
    this APi allows users to:
        - Create, Update, Delete, mark tasks as completed, filter or delete taks by priority & status
    
    Each task has the following structure:
        - id (integer): Unique identifier of the task
        - title (string): Title of the task
        - description (string): Description of the task
        status (string): Status of the task
        - priority (integer): Priority of the task
        - due_date (string): Due date of the task  
"""
    
# import nessesary modules, files & libraries
import os
from flask import Flask, jsonify, request, abort
import tasks_templet as ts
  
# define the api overall function 
app =  Flask(__name__)

# import 'tasks' from 'tasks.py'
tasks = ts.tasks

"""
    # utility function to find task by id
    
    find a task by its uniquw id
    
    parameters: 
    task_id (integer): Unique identifier of the task.
    
    returns:
    dict: task with the given id, or None if not found.
"""

# utility function to find task by id
def task_by_id(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

""" # set enpoint to retrive all tasks

    retríve all tasks
        
    JSON: a list of tasks.
"""
    
# set endpoint to retrive all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

"""
   # set endpoint to retrive a task by id
   
   retrive a specific task by its unique id
   
   parameters: 
   id (int): Unique identifier of the task. 
   
   # retruns
   JSON: task with the given id, or None if not found.
"""

# set endpoint to retrive a task by id
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_by_id(task_id)
    if task:
        return jsonify(task)
    else:
        abort(404)
        
"""
        # set endpoint to create a new task
        
        create a new task
        
        parameters:
        title (string): Title of the task.
        description (string): Description of the task.
        status (string): Status of the task.
        priority (string): Priority of the task.
        due_date (string): Due date of the task.
        
        returns:
        JSON: newly created task
"""
        
# set endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(404)
    new_task = {
        "id": tasks[-1]["id"] + 1,
        "title": request.json["title"],
        "description": request.json["description"],
        "status": request.json["status"],
        "priority": request.json["priority"],
        "due_date": request.json["due_date"]
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

"""
    # set endpoint to update a specific task by its unique id
    
    parameters:
    id (int): Unique identifier of the task.
    
    request JSON body (optional fields):
    - title (string): Title of the task.
    - description (string): Description of the task.
    - status (string): Status of the task.
    - priority (string): Priority of the task.
    - due_date (string): Due date of the task.
    
    returns:
    JSON: updated task
"""

# set endpoint to update a specific task by its unique id
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = get_task(id)
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
        # set endpoint to delete task
        
        delete a specific task by its unique id
        
        parameters:
        id (int): Unique identifier of the task.
        
        returns:
        JSON: deleted task    
"""

# set endpoint to delete task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    task = get_task(task_id)
    if task is None:
        abort(404)
    tasks.remove(task)
    return jsonify(task)

    """
        # set endpoint to mark a specific task
        
        mark a specific task by its unique id
        
        parameters:
        id (int): Unique identifier of the task.
        
        returns:
        JSON: the updated task with status "completed" 
"""
# set endpoint to mark a specific task
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete(task_id):
    task = get_task(task_id)
    if task is None:
        abort(404)
    task["status"] = "completed"
    return jsonify(task)

"""
        # et endpoint to retrieve all completed tasks
        
        retrieve all completed tasks
        
        JSON: a list of completed tasks.
"""

# set endpoint to retrieve all completed tasks
@app.route('/tasks/completed', methods=['GET'])
def get_completed_taskes(task_id):
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    return jsonify(completed_tasks)

"""
        # set endpoint to retrieve all pending tasks
        
        retrive all pending tasks
        
        returns:
        JSON: a list of pending tasks.
"""

# set endpoint to retrieve all pending tasks
@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks(task_id):
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    return jsonify(pending_tasks)

"""
        # set endpoint to retrive tasks by priority level

        retrieve all tasks by priorty level
        
        parameters:
        level (string): Priority level of the tasks, filtered by 'hoch', 'niedrig' or'mittel'.
        
        retrurns:
        JSON: a list of tasks with specified priority level.
"""

# set endpoint to retrive tasks by priority level
@app.route('/tasks/priority/<string:level>', methods=['GET'])
def get_tasks_by_proirity_level(level):
    tasks = [task for task in tasks if task["priority"] == level]
    return jsonify(tasks)

"""
    # set endpoint to delete all clompleted tasks
    
    retrieve all completed tasks
    
    JSON: a list of deleted completed tasks.
"""

# set endpoint to delete all completed tasks
@app.route('/tasks/completed', methods=['GET'])
def delete_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    for task in completed_tasks:
        tasks.remove(task)
    return jsonify(completed_tasks)

"""
    # set endpoint to delete all pending tasks
    
    retrieve all pending tasks
    
    retrurns:
    JSON: a list of deleted pending tasks.
"""

# set endpoint to delete all pending tasks
@app.route('/tasks/pending', methods=['GET'])
def delete_pending_tasks():
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    for task in pending_tasks:
        tasks.remove(task)
    return jsonify(pending_tasks)

# set 'main' function to run the app
if __name__ == "__main__":
    app.run(debug=True)   