from create_app import app
from flask import jsonify, abort, request
from models import Task, User, TaskStatus, TaskType, TaskAttribute, \
    TaskAttributeType, TaskAttributeValue, TaskAttributeToTaskType
from database import db_session
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm.exc import FlushError
from validation.json import validate_json
from validation.query import validate_query
from utils import query_from_dict


@app.route('/task/type/<int:type_id>')
def get_type(type_id):
    task_type = TaskType.query.get(type_id)

    if task_type is None:
        abort(404)

    return jsonify(task_type.to_dict()), 200


@app.route('/task/type/<int:type_id>', methods=['PUT'])
@validate_json('type', 'update')
def update_type(type_id):
    task_type = TaskType.query.get(type_id)

    if task_type is None:
        abort(404)

    data = request.get_json()
    task_type.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Type name must be unique.'), 409

    return jsonify(task_type.to_dict()), 200


@app.route('/task/type', methods=['POST'])
@validate_json('type', 'create')
def create_type():
    data = request.get_json()
    task_type = TaskType.create_from_dict(data)

    db_session.add(task_type)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Type name must be unique.'), 409

    return jsonify(task_type.to_dict()), 201


@app.route('/task/type/<int:type_id>', methods=['DELETE'])
def delete_type(type_id):
    task_type = TaskType.query.get(type_id)

    if task_type is None:
        abort(404)

    db_session.delete(task_type)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        return jsonify(message='Type cannot be deleted'), 409

    return '', 204


@app.route('/task/types')
@validate_query('type', 'query')
def get_types_list():
    query_data = request.args.to_dict()
    types = [task_type.to_dict()
             for task_type in TaskType.query.filter_by(**query_data).all()]

    return jsonify(types), 200


@app.route('/task/types', methods=['POST'])
@validate_json('type', 'search')
def get_types_list_complex():
    data = request.get_json()

    types = [task_type.to_dict()
                  for task_type in query_from_dict(TaskType, data)]

    return jsonify(types), 200
