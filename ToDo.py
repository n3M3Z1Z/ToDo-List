"""
 _____     ____          _     _     _   
|_   _|__ |  _ \  ___   | |   (_)___| |_ 
  | |/ _ \| | | |/ _ \  | |   | / __| __|
  | | (_) | |_| | (_) | | |___| \__ \ |_ 
  |_|\___/|____/ \___/  |_____|_|___/\__|

"""

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
from flask import Flask, jsonify, request
import api_beispieldaten as ts
import datetime
  
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
        return ascii_art_1()
    return jsonify(message="Look at your mess, way to many open tasks, get them done!",tasks=tasks)

"""
    # set endpoint to retrieve task by id
    
    parameters:
    task_id (int): Unique identifier of the task.
    
    returns:
    dict: task with given id
"""

 # Funktion um zu checken, ob auch wirklich ein Wert übergeben wurde
def is_valid_value(value):
    return value not in (None, '', [], {}, ())

def is_valid_status(value):
    right_status = ["pending", "completed"]
    return value in right_status

def is_valid_priority(value):
    right_priority = ["hoch", "mittel", "niedrig"]
    return value in right_priority

# Define function 42 and print ASCII art for most error 400
@app.route('/tasks/function_42', methods=['GET'])
def function_42():
    ascii_art = """
       .                          
                     M                          
                    dM                          
                    MMr                         
                   4MMML                  .     
                   MMMMM.                xf     
   .              "MMMMM               .MM-     
    Mh..          +MMMMMM            .MMMM      
    .MMM.         .MMMMML.          MMMMMh      
     )MMMh.        MMMMMM         MMMMMMM       
      3MMMMx.     'MMMMMMf      xnMMMMMM"       
      '*MMMMM      MMMMMM.     nMMMMMMP"        
        *MMMMMx    "MMMMM\\    .MMMMMMM=         
         *MMMMMh   "MMMMM"   JMMMMMMP           
           MMMMMM   3MMMM.  dMMMMMM            .
            MMMMMM  "MMMM  .MMMMM(        .nnMP"
=..          *MMMMx  MMM"  dMMMM"    .nnMMMMM*  
  "MMn...     'MMMMr 'MM   MMM"   .nMMMMMMM*"   
   "4MMMMnn..   *MMM  MM  MMP"  .dMMMMMMM""     
     ^MMMMMMMMx.  *ML "M .M*  .MMMMMM**"        
        *PMMMMMMhn. *x > M  .MMMM**""           
           ""**MMMMhx/.h/ .=*"                  
                    .3P"%....                   
                  nP"     "*MMnx
    """
    return ascii_art

# define function to call ascii artwork for error 404
def ascii_art_1(): 
    ascii_art_1 = """ .------..
     -          -
   /              \\
 /                   \\
/    .--._    .---.   |
|  /      -__-     \\   |
| |                 |  |
||     ._   _.      ||
||      o   o       ||
||      _  |_      ||
C|     (o\\_/o)     |O     Uhhh, this computer
 \\      _____      /       is like, busted or
   \\ ( /#####\\ ) /       something. So go away.
    \\  `====='  /
     \\  -___-  /
      |       |
      /-_____-\\
    /           \\
  /               \\
 /__|  AC / DC  |__\\
 | ||           |\\ \\
"""
    return ascii_art_1

# Define Endpoint to retrieve task by id
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_by_id(task_id)
    if task:
        return jsonify(message="Congrats you just found yourself a task!", task=task)
    else:
        return ascii_art_1() 

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
        return jsonify({"Fehler": "Request muss im JSON-Format sein - warum muss ich dir das erklären?"}), 400 
    if 'title' not in request.json or 'description' not in request.json:
        return function_42()
    
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
        return jsonify(message="oohpsie whoopsie - you just created yourself more work!", new_task=new_task), 201
    
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
        return ascii_art_1()
    try:
        # nun überprüfe, ob irgendein Key angegeben ist und ersetze ihn, sollte der key auch einen Wert enthalten
        if any(field in request.json for field in ['title', 'status', 'description', 'priority', 'due_date']):
            if 'status' in request.json and not is_valid_status(request.json.get('status')):
                return jsonify({"message": "Nice try. The status is either pending or completed"}), 400
            
            if 'priority' in request.json and not is_valid_priority(request.json.get('priority')):
                return jsonify({"message": "Dude, no! The priority is either hoch, mittel or niedrig."}), 400
            
            task["title"] = request.json.get("title", task["title"]) if is_valid_value(request.json.get("title")) else task["title"]
            task["status"] = request.json.get("status", task["status"]) if is_valid_status(request.json.get("status")) else task["status"]
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
        return ascii_art_1()
    tasks.remove(task)
    return jsonify(message="System32 deleted - bye!", task=task)

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
        return ascii_art_1()
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
        return ascii_art_1()
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
        return ascii_art_1()
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
        return jsonify(message="now look what you did or what you have to to dosent matter to me", priority_tasks=priority_tasks)
    else:
        return function_42()

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
        return ascii_art_1()
    for task in completed_tasks:
        tasks.remove(task)
    return jsonify(message="bye bye files bye bye", completed_tasks=completed_tasks)

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
        return ascii_art_1()
    for task in pending_tasks:
        tasks.remove(task)
    return jsonify(message="Bye Bye files Bye Bye!", pending_tasks=pending_tasks)
    
# Set 'main' function to run the app
if __name__ == "__main__":
    app.run(debug=True)