from flask import Flask, jsonify, abort, make_response, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import Task
from application.app import db
task_api_bp = Blueprint('task_api_bp', __name__)
CORS(task_api_bp)

@task_api_bp.route('/', methods=['GET'])
def home():
    return make_response(jsonify({'tasks': 'Hello World!'}), 200)

@task_api_bp.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        output = []
        for task in tasks:
            task_data = {}
            task_data['id'] = task.id
            task_data['title'] = task.title
            task_data['description'] = task.description
            task_data['done'] = task.done
            output.append(task_data)
        
        response = make_response(jsonify({'tasks': output}), 200)  
        return response
    except:
        abort(500)

@task_api_bp.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return make_response(jsonify({'message':'no record found'}), 404)
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['done'] = task.done
        response = make_response(jsonify({'tasks': task_data}), 200)  
        return response
    except:
        abort(500)

@task_api_bp.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    data = request.json
    try:
        new_task = Task(title=request.json.get('title'), description=request.json.get('description'), done=False)
        db.session.add(new_task)
        db.session.commit()
        task_id = new_task.id
        task = Task.query.get(task_id)
        if not task:
            return make_response(jsonify({'message':'no record found'}), 404)
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['done'] = task.done

        response = make_response(jsonify({'message': 'new task created','tasks': task_data}), 201)  
        return response
    except:
        abort(500)

@task_api_bp.route('/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    if not request.json:
        abort(400)
    if 'title' not in request.json:
        abort(400)
    if 'description' not in request.json:
        abort(400)
    if 'done' in request.json and type(request.json.get('done')) is not bool:
        abort(400)
    try:
        task = Task.query.get(task_id)
        if not task:
            return make_response(jsonify({'message':'no record found'}), 404)  
        task.title = request.json.get('title')
        task.description = request.json.get('description')
        task.done = request.json.get('done')
        db.session.add(task)
        db.session.commit()
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['done'] = task.done

        response = make_response(jsonify({'task': task_data}), 200)  
        return response

    except:
        abort(500)

@task_api_bp.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return make_response(jsonify({'message':'no record found'}), 404) 
        db.session.delete(task)
        db.session.commit()
        return make_response(jsonify({'message': 'Task has been deleted'}), 200)    
    except:
        abort(500)

@task_api_bp.errorhandler(400)
def not_found(error):
    print(error)
    return make_response(jsonify({'error': "Bad request"}), 400)   

@task_api_bp.errorhandler(404)
def handle_404_error(error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': "Not found"}), 400)

@task_api_bp.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)          
