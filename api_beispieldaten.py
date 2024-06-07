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
    
# define the api overall function 
app =  Flask(__name__)

# initialize the tasks list
tasks = [
    {
      "id": 1,
      "title": "Python installieren",
      "description": "Lade die neueste Version von Python von der offiziellen Website herunter und installiere sie.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-10"
    },
    {
      "id": 2,
      "title": "Virtuelle Umgebung einrichten",
      "description": "Lerne, wie man virtuelle Umgebungen mit venv oder virtualenv erstellt und verwaltet.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-11"
    },
    {
      "id": 3,
      "title": "Grundlegende Python-Syntax",
      "description": "Überprüfe die grundlegende Python-Syntax einschließlich Variablen, Schleifen und Bedingungen.",
      "status": "pending",
      "priority": "mittel",
      "due_date": "2024-06-12"
    },
    {
      "id": 4,
      "title": "Python-Datenstrukturen",
      "description": "Lerne über Listen, Wörterbücher, Tupel und Mengen.",
      "status": "pending",
      "priority": "mittel",
      "due_date": "2024-06-13"
    },
    {
      "id": 5,
      "title": "Funktionen in Python",
      "description": "Verstehe, wie man Funktionen in Python definiert und verwendet.",
      "status": "pending",
      "priority": "mittel",
      "due_date": "2024-06-14"
    },
    {
      "id": 6,
      "title": "Objektorientierte Programmierung",
      "description": "Lerne die Grundlagen der objektorientierten Programmierung in Python, einschließlich Klassen und Objekten.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-15"
    },
    {
      "id": 7,
      "title": "Installiere Flask",
      "description": "Installiere Flask, ein leichtgewichtiges Web-Framework für Python.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-16"
    },
    {
      "id": 8,
      "title": "Katzenvideos schauen",
      "description": "Verbringe 30 Minuten mit dem Anschauen von Katzenvideos zur Entspannung.",
      "status": "pending",
      "priority": "niedrig",
      "due_date": "2024-06-17"
    },
    {
      "id": 9,
      "title": "Python und APIs lernen",
      "description": "Erstelle eine einfache Flask-Anwendung mit ein paar Routen.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-18"
    },
    {
      "id": 10,
      "title": "In den Spiegel schauen und sagen: Ich kann das!",
      "description": "Motiviere dich selbst für 5 Minuten vor dem Spiegel.",
      "status": "pending",
      "priority": "mittel",
      "due_date": "2024-06-19"
    },
    {
      "id": 11,
      "title": "Python-Quiz machen",
      "description": "Mache ein Python-Quiz, um dein Wissen zu testen.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-20"
    },
    {
      "id": 12,
      "title": "Tanze wie niemand zusieht",
      "description": "Verbringe 10 Minuten damit, zu deiner Lieblingsmusik zu tanzen.",
      "status": "pending",
      "priority": "niedrig",
      "due_date": "2024-06-21"
    },
    {
      "id": 13,
      "title": "Python-Bücher lesen",
      "description": "Lies ein Kapitel aus einem Python-Buch.",
      "status": "pending",
      "priority": "mittel",
      "due_date": "2024-06-22"
    },
    {
      "id": 14,
      "title": "Ein Bild von einer Python-Schlange zeichnen",
      "description": "Zeichne ein Bild von einer Python-Schlange und hänge es auf.",
      "status": "pending",
      "priority": "niedrig",
      "due_date": "2024-06-23"
    },
    {
      "id": 15,
      "title": "API-Dokumentation lesen",
      "description": "Lies die Dokumentation einer bekannten API.",
      "status": "pending",
      "priority": "mittel",
      "due_date": "2024-06-24"
    },
    {
      "id": 16,
      "title": "Python-Übungen machen",
      "description": "Löse ein paar Python-Übungen auf einer Online-Plattform.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-25"
    },
    {
      "id": 17,
      "title": "Einen Python-Witz lernen",
      "description": "Lerne einen neuen Witz über Python und erzähle ihn deinen Freunden.",
      "status": "pending",
      "priority": "niedrig",
      "due_date": "2024-06-26"
    },
    {
      "id": 18,
      "title": "Kaffee trinken und entspannen",
      "description": "Mache eine Pause, trinke einen Kaffee und entspanne dich.",
      "status": "pending",
      "priority": "niedrig",
      "due_date": "2024-06-27"
    },
    {
      "id": 19,
      "title": "Einen Tag frei nehmen",
      "description": "Nimm dir einen Tag frei von allem Lernen und genieße ihn.",
      "status": "pending",
      "priority": "niedrig",
      "due_date": "2024-06-28"
    },
    {
      "id": 20,
      "title": "Python-Projekt starten",
      "description": "Beginne mit einem kleinen Python-Projekt, das dich interessiert.",
      "status": "pending",
      "priority": "hoch",
      "due_date": "2024-06-29"
    }
]

"""
    # utility function to find task by id
    
    find a task by its uniquw id
    
    parameters: 
    task_id (integer): Unique identifier of the task.
    
    returns:
    dict: task with the given id, or None if not found.
"""

# utility function to find task by id
def task_by_id(task):
    return next((task for task in tasks if task["id"] == task_id), None)

""" # set enpoint to retrive all tasks

    retríve all tasks
        
    JSON: a list of tasks.
"""
    
# set endpoint to retrive all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks(task_id):
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
def create_task(task_id):
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
    task = get_task(task_id)
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