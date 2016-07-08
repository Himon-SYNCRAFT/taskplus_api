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


@app.route('/task/attribute/value/<int:task_id>/<int:task_attribute_id>')
def get_attribute_value(task_id, task_attribute_id):
    attribute_value = TaskAttributeValue.query.get(
        (task_id, task_attribute_id))

    if attribute_value is None:
        abort(404)

    return jsonify(attribute_value.to_dict()), 200


@app.route('/task/attribute/value/<int:task_id>/<int:task_attribute_id>', methods=['PUT'])
@validate_json('attribute_value', 'update')
def update_attribute_value(task_id, task_attribute_id):
    attribute_value = TaskAttributeValue.query.get(
        (task_id, task_attribute_id))

    if attribute_value is None:
        abort(404)

    data = request.get_json()
    attribute_value.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Value for that type already exist for given task.'), 409

    return jsonify(attribute_value.to_dict()), 200


@app.route('/task/attribute/value', methods=['POST'])
@validate_json('attribute_value', 'create')
def create_attribute_value():
    data = request.get_json()
    attribute_value = TaskAttributeValue.create_from_dict(data)

    db_session.add(attribute_value)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Value for that type already exist for given task.'), 409
    except FlushError:
        db_session.rollback()
        return jsonify(message='Value for that type already exist for given task.'), 409

    return jsonify(attribute_value.to_dict()), 201


@app.route('/task/attribute/value/<int:task_id>/<int:task_attribute_id>', methods=['DELETE'])
def delete_attribute_value(task_id, task_attribute_id):
    attribute_value = TaskAttributeValue.query.get(
        (task_id, task_attribute_id))

    if attribute_value is None:
        abort(404)

    db_session.delete(attribute_value)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        return jsonify(message='Value cannot be deleted'), 409

    return '', 204


@app.route('/task/attribute/values')
@validate_query('attribute_value', 'query')
def get_attribute_values_list():
    query_data = request.args.to_dict()
    attribute_values = [attribute_value.to_dict()
                        for attribute_value in TaskAttributeValue.query.filter_by(**query_data).all()]

    return jsonify(attribute_values), 200


@app.route('/task/attribute/values', methods=['POST'])
@validate_json('attribute_value', 'search')
def get_attribute_value_list_complex():
    data = request.get_json()

    attribute_values = [attribute_value.to_dict()
                       for attribute_value in query_from_dict(TaskAttributeValue, data)]

    return jsonify(attribute_values), 200
