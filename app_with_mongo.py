from flask import Flask, jsonify
from flask import abort, request, make_response, url_for
from pprint import pprint
from bson.json_util import dumps
import datetime
import time
import pymongo
import json

#mongoclient import et
#tasks arrayini mongo dbye document olarak insert et
#basic authentication

#MONGO DB processes start here
#STEP1 Read defined variables from json file
with open('config.json') as f:
    config_file = json.load(f)

pprint(config_file)


#Get required values from config
mdb_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = mdb_client[config_file['MONGO_DB']]
my_col = my_db[config_file['MONGO_COLLECTION']]

print(my_db)
print(my_col)

# d = my_col.delete_many({})
# print(d.deleted_count, "documents deleted.")

# insert_data = my_col.insert_many(tasks)

# for f_all in my_col.find():
#     pprint(f_all)

##### Flask API start here
app = Flask(__name__)
version = 1.0

#Get all data
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = my_db.tasks.find()
        return dumps(tasks)
    except Exception as e:
        return dumps({'error': str(e)})
     
#Version
@app.route('/api/version', methods=['GET'])
def get_version():
    return jsonify({'version': version}), 200

#Get specified data by id
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    id_ = my_db.tasks.find_one({'id' : task_id})
    if id_: 
        return dumps(id_)
    #get_task_by_id = [task for task in tasks if task ['id'] == task_id]
    if len(get_task_by_id) == 0:
        abort(404)
    

@app.route('/api/tasks', methods=['POST'])
def post_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'createdate': datetime.datetime.now(),
        'done': False
    }
    my_db.tasks.insert_one(task)


    added_post = my_db.tasks.find_one({'_id': task})
    result = {
        'title': added_post['title'],
        'description': added_post['description'],
        'createdate': added_post['createdate']
    }

    return jsonify({'Message': "Success", 'Result': added_post}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    get_delete_obj = [task for task in tasks if task['id'] == task_id]
    if len(get_delete_obj) == 0:
        abort(404)
    tasks.remove(get_delete_obj[0])
    return jsonify({'result': True})


##Get uri visible for clients
def task_uri_visible(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
