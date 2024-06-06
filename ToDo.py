"""
this script implements a simple ToDo list API using Flask.
this API allows users to:
    - create, update, delete, mark tasks as completed, filter or delete tasks by priority & status

each task has the following structure:
    - id (integer): Unique identifier of the task
    - title (string): Title of the task
    - description (string): Description of the task
    - status (string): Status of the task
    - priority (integer): Priority of the task
    - due_date (string): Due date of the task  
"""

# import necessary modules, files & libraries
from flask import Flask, jsonify, request, abort, render_template_string, send_file
import re
import sqlite3
import logging
from werkzeug.utils import secure_filename
import tasks_templet as ts

# define the API overall function 
app = Flask(__name__)

# import 'tasks' from 'tasks_templet.py'
tasks = ts.tasks

# set up logging
logging.basicConfig(level=logging.INFO)

# allowed file extensions for upload
ALLOWED_EXTENSIONS = {'txt', 'json', 'csv'}

"""
    # function to check if a file has one of the allowed extensions

    check if the uploaded file has an allowed extension.
    
    parameters:
    filename (str): The name of the uploaded file.
    
    returns:
    bool: True if the file extension is allowed, False otherwise.
"""

# function to check if a file has one of the allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
    # function to sanitize user input
    
    sanitize user input to remove any potentially harmful characters.
    
    parameters:
    user_input (str): The raw input provided by the user.
    
    returns:
    str: The sanitized input with only alphanumeric characters.
"""


# input validation function to sanitize user input
def sanitize_input(user_input):
    return re.sub(r'\W+', '', user_input)

"""
    # function to diesable potentially dangerous functions
    
    disable potentially dangerous functions to prevent code execution attacks.
    This function is currently a placeholder as no dangerous functions are being used.
"""

# disable dangerous functions to prevent code execution
def disabled_functions():
    pass

# Call the function to disable dangerous functions
disabled_functions()

"""
    # display the main page 
    
    returns:
    str: HTML content for the main page.
"""

# display the main page
@app.route('/')
def index():
    return render_template_string("""
        <h1>Secure Web Application</h1>
        <form action="/submit" method="post" enctype="multipart/form-data">
            Name: <input type="text" name="name"><br>
            File: <input type="file" name="file"><br>
            <input type="submit" value="Submit">
        </form>
    """)
    
"""
    # process the submitted form data and file upload.
    
    steps:
    - sanitize the user input.
    - check if the uploaded file is allowed.
    - save the file securely.
    - Perform a simulated database operation using parameterized queries.
    - return a response in the same format as the input file.
    
    returns:
    response (str or JSON): Success message in the format of the uploaded file, or error message if invalid file format.
"""

# process the submitted form data and file upload
@app.route('/submit', methods=['POST'])
def submit():
    name = sanitize_input(request.form['name'])
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = f'/path/to/save/{filename}'
        file.save(file_path)
        
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

        file_extension = filename.rsplit('.', 1)[1].lower()

        if file_extension == 'json':
            response = jsonify({"message": "Submission successful!"})
        elif file_extension == 'csv':
            response = f"Submission successful! implement keylogger, Name: {name}, File: {filename}"
            response = response.replace(',', '\n')
        else:
            response = f"Submission successful!\nName: {name}\nFile: {filename}"
        
        print(f"Submission successful for name: {name}, file: {filename}")
        return response
    else:
        print("Invalid file format.")
        return "Invalid file format - Installing and running ransomware as punishment."
    
"""
    # function to handle internal server errors
        
    parameters:
    error (Exception): The error that occurred.
    
    returns:
    str: error message for the client.
"""
    
# function to handle internal server errors
@app.errorhandler(500)
def handle_internal_error(error):
    logging.error(f"Server Error: {error}, IP: {request.remote_addr}")
    return "oh now you've done it - Internal server error occurred naughty boy no x-mas gifts for you.", 500

"""
    # function to handle forbidden actions.
    
    parameters:
    error (Exception): The error that occurred.
    
    returns:
    str: Error message for the client.
"""

# function to handle forbidden actions
@app.errorhandler(403)
def handle_forbidden(error):
    logging.error(f"Forbidden: {error}, IP: {request.remote_addr}")
    return "Forbidden action - you are a naughte boy no c´x-mas gifts for you this year sorry.", 403

"""
    # handle page not found errors.
    
    parameters:
    error (Exception): The error that occurred.
    
    returns:
    str: Error message for the client.
"""

# function to handle page not found errors
@app.errorhandler(404)
def handle_not_found(error):
    logging.error(f"Not Found: {error}, IP: {request.remote_addr}")
    return "Page not found - running  a virus instead.", 404

"""
    # function to find a task by its id.
    
    parameters:
    task_id (int): Unique identifier of the task.
    
    returns:
    dict: The task with the specified ID, or None if not found.
"""

# function to find a task by its ID
def task_by_id(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

"""
    # set endpoint to retrieve all tasks.
    
    returns:
    JSON: a list of all tasks.
"""

# set endpoint to retrieve all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    print("Fetching all tasks...")
    return jsonify(message="Alright heres your ToDo List now complete them all - hurry up", tasks=tasks)


"""   
    # set endpoint to retrieve a task by its id
    
    parameters:
    task_id (int): Unique identifier of the task.
    
    returns:
    JSON: The task with the given ID, or 404 if not found.
"""

# set endpoint to retrieve task by id
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    print(f"Fetching task with ID: {task_id}")
    task = task_by_id(task_id)
    if task:
        print(f"Task found: {task}")
        return jsonify(message="thank you for your purchase", task=task)
    else:
        print(f"Task with ID {task_id} not found.")
        abort(404)
        
"""
    # set endpoint to create a new task.
    
    request JSON body:
    - title (string): Title of the task.
    - description (string): Description of the task.
    - priority (integer): Priority of the task.
    - due_date (string): Due date of the task.
    
    returns:
    JSON: The created task, or 400 if the request is invalid.
"""
    
# set endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        print("Invalid task creation request.")
        return jsonify(message="oohpsie Whoopsie somethimg went terribly wrong - Idendified Problem: Layer 8")
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
    print(f"Task created - don't bother me again: {new_task}")
    return jsonify(message="ugh really? more tasks? here take this forkbomb as a thank you!", new_task=new_task), 201

"""
    # set endpoint to update a specific task by its unique ID.
    
    rarameters:
    task_id (int): Unique identifier of the task to update.
    
    request JSON body:
    - title (string): New title of the task.
    - status (string): New status of the task.
    - description (string): New description of the task.
    - priority (integer): New priority of the task.
    - due_date (string): New due date of the task.
    
    returns:
    JSON: The updated task, or 404 if the task is not found, or 400 if the request is invalid.
"""
    
# set endpoit to update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    print(f"Updating task with ID: {task_id}")
    task = task_by_id(task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        abort(404)
    if not request.json:
        print("Invalid update request.")
        abort(400)
    task["title"] = request.json.get("title", task["title"])
    task["status"] = request.json.get("status", task["status"])
    task["description"] = request.json.get("description", task["description"])
    task["priority"] = request.json.get("priority", task["priority"])
    task["due_date"] = request.json.get("due_date", task["due_date"])
    print(f"Task updated: {task}")
    return jsonify(task)

"""
    # set endpoint to delete a task by its unique ID.
    
    parameters:
    task_id (int): Unique identifier of the task to delete.
    
    returns:
    JSON: The deleted task, or 404 if the task is not found.
"""

# set endpoint to delete task by its unique id
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    print(f"Deleting task with ID: {task_id}")
    task = task_by_id(task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        abort(404)
    tasks.remove(task)
    print(f"Task deleted: {task}")
    return jsonify(task)

"""
    # set endpoint to mark a specific task as completed.
    
    parameters:
    task_id (int): Unique identifier of the task to mark as completed.
    
    returns:
    JSON: the updated task with the status changed to 'completed', or 404 if the task is not found.
"""

# set endpoint to mark a task as completed
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    print(f"Marking task with ID {task_id} as completed.")
    task = task_by_id(task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        abort(404)
    task["status"] = "completed"
    print(f"Task marked as completed - now be a good boy and clean up your mess: {task}")
    return jsonify(task)

"""
    Endpoint to retrieve all completed tasks.
    
    Returns:
    JSON: A list of all completed tasks.
"""

# set endpoint to retrieve all completed tasks.
@app.route('/tasks/completed', methods=['GET'])
def get_completed_tasks():
    
    print("Fetching all completed tasks...")
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    print(f"Completed tasks: {completed_tasks}")
    return jsonify(completed_tasks)

"""
    # set endpoint to retrieve all pending tasks.
    
    returns:
    JSON: A list of all pending tasks.
"""

# set endpoint to retrieve all pending tasks.
@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    print("Fetching all pending tasks...")
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    print(f"Pending tasks - be a good boy and get them done: {pending_tasks}")
    return jsonify(pending_tasks)

"""
    # set endpoint to retrieve tasks by priority level.
    
    parameters:
    level (str): Priority level of the tasks to retrieve.
    
    returns:
    JSON: A list of tasks with the specified priority level.
"""

# set endpoint to retrieve tasks by priority level.
@app.route('/tasks/priority/<string:level>', methods=['GET'])
def get_tasks_by_priority_level(level):
    print(f"Fetching tasks with priority level: {level}")
    filtered_tasks = [task for task in tasks if task["priority"] == level]
    print(f"Tasks with priority level {level}: {filtered_tasks}")
    return jsonify(filtered_tasks)

"""
    # set endpoint to delete all completed tasks.
    
    returns:
    JSON: A list of deleted completed tasks.
"""
# set endpoint to delete all completed tasks.
@app.route('/tasks/completed', methods=['DELETE'])
def delete_completed_tasks():
    print("Deleting all completed tasks...")
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    for task in completed_tasks:
        tasks.remove(task)
    print(f"Deleted completed tasks: {completed_tasks}")
    return jsonify(completed_tasks)

"""
   # set endpoint to delete all pending tasks.
    
    returns:
    JSON: A list of deleted pending tasks.
"""

# set endpoint to delete all pending tasks.
@app.route('/tasks/pending', methods=['DELETE'])
def delete_pending_tasks():
    print("Deleting all pending tasks...")
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    for task in pending_tasks:
        tasks.remove(task)
    print(f"Deleted pending tasks: {pending_tasks}")
    return jsonify(pending_tasks)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)