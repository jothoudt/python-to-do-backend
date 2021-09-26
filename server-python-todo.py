import flask
import psycopg2
from flask import request, jsonify
from psycopg2.extras import RealDictCursor
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"]= True

connection=psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="python_todo"
)
# Test homepage for the server
@app.route('/', methods=['GET'])
def home():
  return "<h1>To-do server</h1>"

# This route is to get all of the tasks from the database
@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    cursor= connection.cursor(cursor_factory=RealDictCursor)
    # Database GET query
    postgreSQL_fetch_query= "SELECT * FROM todo;"
    # execute query
    cursor.execute(postgreSQL_fetch_query)
    taskList=cursor.fetchall()
    return jsonify(taskList)
# This route is to add a task to the database
@app.route('/api/tasks', methods=['POST'])
def create_task():
    print('using multipart from data', request.json['task'])
    task=request.json['task']

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        print(task)
        # Database POST query
        postgreSQL_addTask_Query= "INSERT INTO todo (task) VALUES (%s); "
        # execute query
        cursor.execute(postgreSQL_addTask_Query, (task,))
        connection.commit()
        count=cursor.rowcount
        print(count, "task inserted")
        result = {'status':'CREATED'}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert task")
        result = {'status' : 'ERROR'}
        return jsonify(result), 500
    finally:
        if(cursor):
            cursor.close()
# This route is to delete a task from the database
@app.route('/api/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    print  ('in delete task')
    id= id
    try:
        cursor=connection.cursor(cursor_factory=RealDictCursor)
        print(id)
        # Database DELETE query
        postgreSQL_delete_query= "DELETE FROM todo WHERE id=(%s)"
        # Execute query
        cursor.execute(postgreSQL_delete_query, (id,))
        connection.commit()
        count=cursor.rowcount
        print(count, 'task deleted')
        result={'status': 'deleted'}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        print('Failed to delete task', error)
        result={'status': 'ERROR'}
        return jsonify(result), 500
    finally:
        if(cursor):
            cursor.close()
# This rout is to update a task in the database to complete
@app.route('/api/tasks/<id>', methods=['PUT'])
def update_task(id):
    print('in complete task')
    id= id
    datetime.datetime.now()
    timestamp=datetime.datetime.now()
    print(timestamp)
    try:
        cursor=connection.cursor(cursor_factory=RealDictCursor)
        print(id)
        # Database PUT query
        postgreSQL_update_query= "UPDATE todo SET completed=TRUE, date_completed = (%s) WHERE id=(%s);"
        # execute query
        cursor.execute(postgreSQL_update_query, (timestamp, id,))
        connection.commit()
        count=cursor.rowcount
        print(count, 'task updated')
        result={'status':'updated'}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        print('Failed to update task', error)
        result = {'status': 'ERROR'}
        return jsonify(result), 500
    finally:
        if(cursor):
            cursor.close()   


app.run()