from create_app import app
from flask import jsonify, abort, request
from models import Task, User, Task, TaskType, TaskAttribute, \
    TaskAttributeType, TaskAttributeValue, TaskAttributeToTaskType
from database import db_session
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm.exc import FlushError
from validation.json import validate_json
from validation.query import validate_query
from utils import query_from_dict


@app.route('/task/<int:task_id>')
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)

    return jsonify(task.to_dict()), 200


@app.route('/task/<int:task_id>', methods=['PUT'])
@validate_json('task', 'update')
def update_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        abort(404)

    data = request.get_json()
    task.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        return jsonify(dict(message=str(e))), 409

    return jsonify(task.to_dict())


@app.route('/task', methods=['POST'])
@validate_json('task', 'create')
def create_task():
    data = request.get_json()
    task = Task.create_from_dict(data)

    try:
        db_session.add(task)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        return jsonify(dict(message=str(e))), 409

    return jsonify(task.to_dict()), 201


@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        abort(404)

    db_session.delete(task)

    try:
        db_session.commit()
    except (IntegrityError, AssertionError):
        db_session.rollback()
        return jsonify(dict(message='Task cannot be deleted')), 409

    return '', 204


@app.route('/tasks')
@validate_query('task', 'query')
def get_tasks_list():
    tasks = [task.to_dict()
                for task in Task.query.filter_by(**request.args.to_dict()).all()]

    return jsonify(tasks), 200


@app.route('/tasks', methods=['POST'])
@validate_json('task', 'search')
def get_tasks_list_complex():
    data = request.get_json()

    tasks = [task.to_dict()
                for task in query_from_dict(Task, data)]

    return jsonify(tasks), 200
