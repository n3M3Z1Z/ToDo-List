"""
 _____     ____          _     _     _   
|_   _|__ |  _ \  ___   | |   (_)___| |_ 
  | |/ _ \| | | |/ _ \  | |   | / __| __|
  | | (_) | |_| | (_) | | |___| \__ \ |_ 
  |_|\___/|____/ \___/  |_____|_|___/\__|

"""

"""
*This script implements a simple ToDo list API using Flask.*

For personalisatiion this API will ask you for the following information:
- name

This enables the API to address the user by her or his name.

To optimize the "expirience" higly recommend usind the 'Postman' app,
 which allows you to send requests to the API. 
 
 To further optimize the "expirience" you should view the rusult of your requests
 in the 'raw' view of the output window.
 
 Postman can be downloaded here: https://www.postman.com/downloads/

*This API allows users to:*
    - Create
    - Update 
    - delete
    - mark tasks as completed
    - filter or delete tasks by priority & status
    - upload json files
    - download json files

*Each task has the following structure:*
    - id (integer): Unique identifier of the task
    - title (string): Title of the task
    - description (string): Description of the task
    - status (string): Status of the task
    - priority (integer): Priority of the task
    - due_date (string): Due date of the task  
    
*This API has following endpoints:*
    - home: the main page of the API with explicit instructions on how to use the API
    - tasks: amount vary according to the amount of tasks in the 'tasks' list
    - completed: all completed tasks are displayed here until they are deleted
    - pending: all pending tasks are displayed here until they are either completed or deleted
    - upload: upload a json file containing tasks in json file format
    - download: download a json file containing tasks in json file format
    - endpoint_42: the place to go if you need to relax ;)
    - awsome: See somethinf really awesome
    
*Following operations can be performed on the tasks:*
    - 'GET': navigate to the specifed endpoint or the given task id
    - 'POST': create a new task
    - 'PUT': update a task
    - 'DELETE': delete a task
    
*Possible errors:*
    - 400: Bad Request
    - 404: Not Found
    - invalied input
    - forbidded operation
    - syntax error
    - Datetime format error
    - invalied id
    - invalied priority
    - invalid status
    - invalied due date
    
*Error handling.+
    - 400: Bad Request: The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat
    - 404: Not Found: The requested resource could not be found but may be available again. Client SHOULD NOT repeat the request without modifications.
    - 405: Method Not Allowed: The request method is known by the server but has been disabled and cannot be used. Client SHOULD NOT repeat the request without modifications.
    
*To be able to use this phenomemal and awesome API you need:*
    - a python in
    - flask module (Flask, jasonify, request, g)
    - datetime module
    - an json file containing tasks in json file format (in this file called: 'api_beispieldaten')
    - os module

*We added extened documentation for some endpoints as well as for most of the functions.*
    
*For more information on how to use this API please read our documentation pdf file in this repository.*
"""

# Import necessary modules, files & libraries
from flask import Flask, jsonify, request, g
import api_beispieldaten as ts
from datetime import datetime
import os
  
# Define the API overall function 
app = Flask(__name__)

# Import 'tasks' from 'tasks_templet.py'
tasks = ts.tasks

# ask for the user's name
@app.route("/user", methods=["GET"])
def get_user_name():
    user_name = input("Please enter your name: ")
    user_name = "Zipfelklatscher"
    return jasonify(message=f"Welcome {user_name} enjoy our API!")

# set 'home' endpoint
@app.route("/home", methods=["GET"])
def home():
    home_content = {
        "message": "Welcome to the ToDo List API {user_name}!",
        "actions": [
            "- create a new task",
            "- update an existing task",
            "- delete an existing task",
            "- mark a task as completed",
            "- filter or delete tasks by priority & status",
            "- upload a json file containing tasks in json file format",
            "- download a json file containing tasks in json file format",
        ],
        "endpoints": {
            "tasks": "/home/tasks" "- to display all tasks",
            "completed": "/home/completed" "- to display all completed tasks",
            "pending": "/home/pending" "- to display all pending tasks",
            "upload": "/home/upload" "- to upload a json file",
            "download": "/home/download" "- to download a json file",
            "endpoint_42": "/home/endpoint_42" "- the place to go if you need to relax ;)",
            "awsome": "/home/awsome" "- see something awsome",
        }
    }
    return jsonify(home_content), 200
"""
    *set endpoint to retrieve task by id*
    
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

# ist der Staus der eingegeben wurde, valide
def is_valid_status(value):
    right_status = ["pending", "completed"]
    return value in right_status

# ist die Priorität valide
def is_valid_priority(value):
    right_priority = ["hoch", "Hoch", "mittel", "Mittel", "niedrig", "Niedrig"]
    return value in right_priority

def parse_and_validate_due_date(due_date_str):
    possible_formats = ["%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y", "%d-%m-%Y"]
    for fmt in possible_formats:
        try:
            due_date = datetime.strptime(due_date_str, fmt)
            if due_date > datetime.now():
                return due_date.strftime("%Y-%m-%d")
            else:
                return False
        except ValueError:
            continue
    return False 


"""
    *set endpoint to retrieve all tasks*
    
    retrieve all tasks
    
    returns:
    JSON: a list of all tasks.
"""

# Set endpoint to retrieve all tasks
@app.route("/home/tasks", methods=["GET"])
def get_tasks():
    if not tasks:
        return error_404()
    return jsonify(message=f"{user_name} look at your mess, way to many open tasks, get them done!",tasks=tasks)

"""
    *set endpoint to retrieve task by id*
    
    parameters:
    task_id (int): Unique identifier of the task.
    
    returns:
    dict: task with given id
"""


# set and define endpoint_42 and print ASCII art for most error 400
@app.route('/home/endpoint_42', methods=['GET'])
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
      3MMMMx.     'MMMMMMf      xnMMMMMM"      chill Bro.....
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

# define function to call ascii artwork for error 404 - Page not found
def error_404(): 
    error_404 = """ .------..
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
   \\ ( /#####\\ ) /       something {user_name}. So go away.
    \\  `====='  /
     \\  -___-  /
      |       |            Error 404, page not found.
      /-_____-\\
    /           \\
  /               \\
 /__|  AC / DC  |__\\
 | ||           |\\ \\
"""
    return error_404

# define function to call ascii artwork for error 400  - Bad Request (at least some of them)
def error_400():
    error_400 = """
     .'/,-Y"     "~-.  
 l.Y             ^.           
 /\               _\_      "DOH!"   
i            ___/"   "\ 
|          /"   "\   o !   
l         ]     o !__./   
 \ _  _    \.___./    "~\  
  X \/ \            ___./  
 ( \ ___.   _..--~~"   ~`-.  
  ` Z,--   /               \    
    \__.  (   /       ______) 
      \   l  /-----~~" /      Error 400, Bad Request
       Y   \          / 
       |    "x______.^  Try again, {user_name}
       |           \    
       j            Y
"""
    return error_400

# define function to call ascii artwork for error 405 - Method Not Allowed
def error_405():
    error_405 = """
     |____________|_
   ||--------|| | _________
   ||- _     || |(Bye Bye )
   ||    - _ || | ---------
   ||       -|| |     //
   ||        || O\    __
   ||        ||  \\  (..)
   ||        ||   \\_|  |_
   ||        ||    \  \/  )
   ||        ||     :    :|
   ||        ||     :    :|
   ||        ||     :====:O
   ||        ||     (    )
   ||__@@@@__||     | `' |
   || @|..|@ ||     | || |
   ||O@`=='@O||     | || |
   ||_@\/\/@_||     |_||_|
 ----------------   '_'`_`
/________________\----------\
|   GUILLOTINE   |-----------|
 Error 405, Method Not Allowed
|____________________________|
You are not allowed to do that, {user_name}
"""
    return error_405

# Define Endpoint to retrieve task by id
@app.route("/home/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_by_id(task_id)
    if task:
        return jsonify(message=f"Congrats {user_name} you just found yourself a task!", task=task)
    else:
        return error_404() 

"""
    *set endpoint to create a new task*
    
    request JSON body:
    - title (string): Title of the task.
    - description (string): Description of the task.
    - priority (integer): Priority of the task.
    - due_date (string): Due date of the task.
"""

# Set endpoint to create a new task
@app.route('/home/tasks', methods=['POST'])
def create_task():
    try:
        request_json = request.get_json(force=True)
    except Exception as e:
        return jsonify({"Fehler": f"Failed to decode JSON object: {str(e)}"}), 400
    
    #if not request.json:
    #    return jsonify({"Fehler": "Request muss im JSON-Format sein"}), 400 
    if 'title' not in request.json or 'description' not in request.json:
        return jsonify({"Fehler": "Es müssen sowohl der title, wie auch die description gesetzt sein. Sollstest du eigent wissen"}), 400
    
    due_date_str = request.json.get("due_date")
    if due_date_str:
        due_date = parse_and_validate_due_date(due_date_str)
        if not due_date:
            return jsonify({"Fehler": "Due date must be in the future and in a valid format (YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY, or DD-MM-YYYY)"}), 400
    else:
        due_date = None


    if 'status' in request.json and not is_valid_status(request.json.get('status')):
              return jsonify({"message": "Nice try. The status is either pending or completed"}), 400
    
    if 'priority' in request.json and not is_valid_priority(request.json.get('priority')):
        return jsonify({"message": "Dude, no! The priority is either hoch, mittel or niedrig."}), 400
    try:
        new_task = {
            "id": tasks[-1]["id"] + 1,
            "title": request_json["title"],
            "description": request_json["description"],
            "status": request_json.get("status", "pending"), # Default value is pending
            "priority": request_json.get("priority", "niedrig"),
            "due_date": request_json.get("due_date", None)
        }
        tasks.append(new_task)
        return jsonify(message=f"oohpsie whoopsie - {user_name} you just created yourself more work!", new_task=new_task), 201
    
    except Exception as e:
        return jsonify({"Fehler": str(e)}), 400

"""
    *set endpoint to update a specific task*
    
    parameters: 
    id (int): Unique identifier of the task.
    
    returns:
    JSON: updated task
"""

# Set endpoint to update a specific task by its unique id
@app.route('/home/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = task_by_id(task_id)
    # schaue ob der Task existiert
    if task is None:
        return error_404()
    try:
        # nun überprüfe, ob irgendein Key angegeben ist und ersetze ihn, sollte der key auch einen Wert enthalten
        if any(field in request.json for field in ['title', 'status', 'description', 'priority', 'due_date']):
            if 'status' in request.json and not is_valid_status(request.json.get('status')):
                return jsonify({"message": f"Nice try {user_name} . The status is either pending or completed"}), 400
            
            if 'priority' in request.json and not is_valid_priority(request.json.get('priority')):
                return jsonify({"message": f"Dude, no! The priority is either hoch, mittel or niedrig."}), 400
            
            if 'id' in request.json:
                return jsonify({"message": "No, i want to keep my ID."})
            
            if 'due_date' in request.json:
                due_date_str = request.json.get("due_date")
                if due_date_str:
                    due_date = parse_and_validate_due_date(due_date_str)
                    if not due_date:
                        return jsonify({"Fehler": "Due date must be in the future and in a valid format (YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY, or DD-MM-YYYY)"}), 400
                else:
                    due_date = None
            task["title"] = request.json.get("title", task["title"]) if is_valid_value(request.json.get("title")) else task["title"]
            task["status"] = request.json.get("status", task["status"]) if is_valid_status(request.json.get("status")) else task["status"]
            task["description"] = request.json.get("description", task["description"]) if is_valid_value(request.json.get("description")) else task["description"]
            task["priority"] = request.json.get("priority", task["priority"]) if is_valid_value(request.json.get("priority")) else task["priority"]
            task["due_date"] = request.json.get("due_date", task["due_date"])if is_valid_value(request.json.get("due_date")) else task["due_date"]
            return jsonify(message="know what? find the error yourself! Good Luck!", task=task)
        
    except Exception as e:
        return jsonify({"Zipfelklatscher": str(e)}), 400

"""
    *set endpoint to delete tasks*
    
    parameters: 
    id (int): Unique identifier of the task.
    
    returns:
    JSON: deleted task
"""

# Set endpoint to delete task
@app.route('/home/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = task_by_id(task_id)
    if task is None:
        return error_404()
    tasks.remove(task)
    return jsonify(message="System32 deleted - bye!", task=task)

"""
    *set endpont to mark a specific task as deleted*
    
    parameters: 
    id (int): Unique identifier of the task.
    
    returns:
    JSON: deleted task
"""

# Set endpoint to mark a specific task
@app.route('/home/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = task_by_id(task_id)
    if task is None:
        return error_404()
    task["status"] = "completed"
    return jsonify(Message=f"{user_name} you marked it you do it! I'll check it!", task=task)

"""
    *set endpoint to retrieve all completed tasks*
    
    retruns:
    JSON: a list of all completed tasks.
"""

# Set endpoint to retrieve all completed tasks
@app.route('/home/tasks/completed', methods=['GET'])
def get_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    if not completed_tasks:
        return error_404()
    return jsonify(message=f"You are a very good boy {user_name}!", completed_tasks=completed_tasks)

"""
    *set endpoint to retieve all pending tasks*
    
    returns:
    JSON: a list of all pending tasks.
"""

# Set endpoint to retrieve all pending tasks
@app.route('/home/tasks/pending', methods=['GET'])
def get_pending_tasks():
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    if not pending_tasks:
        return error_404()
    return jsonify(message="Do or do not - there is no pending!", pending_tasks=pending_tasks)

"""
    *set endpoint to retrieve tasks by priority level*
    
    parameters:
    level (string): Priority level of the task.
    
    returns:
    JSON: a list of tasks with specified priority level.
"""

# Set endpoint to retrieve tasks by priority level
@app.route('/home/tasks/priority/<string:level>', methods=['GET'])
def get_tasks_by_proirity_level(level):
    level_list = ["hoch", "niedrig", "mittel"]
    if level in level_list:
        priority_tasks = [task for task in tasks if task["priority"] == level]
        return jsonify(message=f"now look what you did {user_name} or what you have to to dosen't really matter to me", priority_tasks=priority_tasks)
    else:
        return error_400()

"""
    *set endpoint to delete all completed tasks*
    
    retrurns:
    JSON: a list of deleted completed tasks.
"""

# Set endpoint to delete all completed tasks
@app.route('/home/tasks/completed', methods=['DELETE'])
def delete_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "completed"]
    if not completed_tasks:
        return error_404()
    for task in completed_tasks:
        tasks.remove(task)
    return jsonify(message=f"say bye bye files {user_name} bye bye", completed_tasks=completed_tasks)

"""
    *set endpoint to delete all pending tasks*
    
    retrurns:
    JSON: a list of deleted pending tasks.
"""

# Set endpoint to delete all pending tasks
@app.route('/home/tasks/pending', methods=['DELETE'])
def delete_pending_tasks():
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    # wenn keine Tasks in pending vorliegen
    if not pending_tasks:
        return error_404()
    for task in pending_tasks:
        tasks.remove(task)
    return jsonify(message=f"say bye bye files {user_name} bye bye!", pending_tasks=pending_tasks)
  
# Set endpoint to upload json files (Honeypot 1)
@app.route('/home/upload', methods=['POST'])
def upload():
    upload = """
        __        __   _                            _                           
\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___     ___  _   _ _ __ 
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \   / _ \| | | | '__|
  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | (_) | |_| | |   
 _ \_/\_/_\___|_|\___\___/|_| |_|_|_|\___|_ \__\___/   \___/ \__,_|_|   
| | | |/ _ \| \ | \ \ / /  _ \ / _ \_   _| |                            
| |_| | | | |  \| |\ V /| |_) | | | || | | |                            
|  _  | |_| | |\  | | | |  __/| |_| || | |_|                            
|_|_|_|\___/|_| \_| |_| |_|    \___/ |_| (_)        _ _                 
|  _ \(_) __| |  _   _  ___  _   _   _ __ ___  __ _| | |_   _           
| | | | |/ _` | | | | |/ _ \| | | | | '__/ _ \/ _` | | | | | |          
| |_| | | (_| | | |_| | (_) | |_| | | | |  __/ (_| | | | |_| |          
|____/|_|\__,_|  \__, |\___/ \__,_| |_|  \___|\__,_|_|_|\__, |          
 _   _     _     |___/                                  |___/_     _    
| |_| |__ (_)_ __ | | __ __      _____  __      _____  _   _| | __| |   
| __| '_ \| | '_ \| |/ / \ \ /\ / / _ \ \ \ /\ / / _ \| | | | |/ _` |   
| |_| | | | | | | |   <   \ V  V /  __/  \ V  V / (_) | |_| | | (_| |   
 \__|_| |_|_|_| |_|_|\_\   \_/\_/ \___|   \_/\_/ \___/ \__,_|_|\__,_|   
| |__   ___   ___  ___     ___ __ _ _ __ ___| | ___  ___ __|__ \        
| '_ \ / _ \ / __|/ _ \   / __/ _` | '__/ _ \ |/ _ \/ __/ __|/ /        
| |_) |  __/ \__ \ (_) | | (_| (_| | | |  __/ |  __/\__ \__ \_|         
|_.__/ \___| |___/\___/   \___\__,_|_|  \___|_|\___||___/___(_)  
"""
    return upload

# set endpoint for download json file (Honeypot 2)
@app.route('/home/download', methods=['GET'])
def download():
    download = """
        _    _ _                             __ _ _           
   / \  | | |  _   _  ___  _   _ _ __   / _(_) | ___  ___ 
  / _ \ | | | | | | |/ _ \| | | | '__| | |_| | |/ _ \/ __|
 / ___ \| | | | |_| | (_) | |_| | |    |  _| | |  __/\__ \
/_/   \_\_|_|  \__, |\___/ \__,_|_|    |_| |_|_|\___||___/
| |__   __ ___ |___/__  | |__   ___  ___ _ __             
| '_ \ / _` \ \ / / _ \ | '_ \ / _ \/ _ \ '_ \            
| | | | (_| |\ V /  __/ | |_) |  __/  __/ | | |           
|_| |_|\__,_| \_/ \___| |_.__/ \___|\___|_| |_| _         
  ___ _ __   ___ _ __ _   _ _ __ | |_ ___  __| | |        
 / _ \ '_ \ / __| '__| | | | '_ \| __/ _ \/ _` | |        
|  __/ | | | (__| |  | |_| | |_) | ||  __/ (_| |_|        
 \___|_| |_|\___|_|   \__, | .__/ \__\___|\__,_(_)      
"""
    return download

# set an 'awsome' endpoint
@app.route('/home/awsome')
def awsome(): 
    awsome = """
             _nnnn_                      
        dGGGGMMb     ,"""""""""""""".
       @p~qp~~qMb    | Linux Rules! |
       M|@||@) M|   _;..............'
       @,----.JM| -'
      JS^\__/  qKL
     dZP        qKRb    and so do this awsome peapole that created this app!
    dZP          qKKb
   fZP            SMMb      Svea Kristina Wilkening
   HZM            MMMM          Tamina Adam
   FqM            MMMM              Markus Bacher
 __| ".        |\dS"qML                 Georg Gohmann
 |    `.       | `' \Zq                      Michael Herz
_)      \.___.,|     .'
\____   )MMMMMM|   .' And last but not least a big thank you to our
     `-'       `--'   awsome victim eehhm i mean teacher 'Andreas Thomas Kellerer'
 """
    return awsome

# Function to handle 400 Bad Request error
@app.errorhandler(400)
def bad_request(error):
    return error_400()

# Function to handle 404 Not Found error
@app.errorhandler(404)
def page_not_found(error):
    return error_404()

# Function to handle 405 Method Not Allowed error
@app.errorhandler(405)
def method_not_allowed(error):
    return error_405()

# Set 'main' function to run the app
if __name__ == "__main__":
    app.run(debug=True)