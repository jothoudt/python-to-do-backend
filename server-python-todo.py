import flask
import psycopg2
from flask import request, jsonify
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"]= True

connection=psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="python_todo"
)
@app.route('/', methods=['GET'])
def home():
  return "<h1>To-do server</h1>"

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    cursor= connection.cursor(cursor_factory=RealDictCursor)

    postgreSQL_fetch_query= "SELECT * FROM todo"

    cursor.execute(postgreSQL_fetch_query)

    taskList=cursor.fetchall()

    return jsonify(taskList)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    print('using multipart from data', request.json['task'])
    task=request.json['task']

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        print(task)

        postgreSQL_addTask_Query= "INSERT INTO todo (task) VALUES (%s); "
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

app.run()