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


@app.route('/task/attribute-to-type/<int:task_type_id>/<int:task_attribute_id>')
def get_attribute_to_type(task_type_id, task_attribute_id):
    attribute_to_type = TaskAttributeToTaskType.query.get(
        (task_type_id, task_attribute_id))

    if attribute_to_type is None:
        abort(404)

    return jsonify(attribute_to_type.to_dict()), 200


@app.route('/task/attribute-to-type/<int:task_type_id>/<int:task_attribute_id>', methods=['PUT'])
@validate_json('attribute_to_type', 'update')
def update_attribute_to_type(task_type_id, task_attribute_id):
    attribute_to_type = TaskAttributeToTaskType.query.get(
        (task_type_id, task_attribute_id))

    if attribute_to_type is None:
        abort(404)

    data = request.get_json()
    attribute_to_type.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        return jsonify(message=str(e)), 409

    return jsonify(attribute_to_type.to_dict()), 200


@app.route('/task/attribute-to-type', methods=['POST'])
@validate_json('attribute_to_type', 'create')
def create_attribute_to_type():
    data = request.get_json()
    attribute_to_type = TaskAttributeToTaskType.create_from_dict(data)

    db_session.add(attribute_to_type)

    try:
        db_session.commit()
    except (IntegrityError, FlushError) as e:
        db_session.rollback()
        return jsonify(message=str(e)), 409

    return jsonify(attribute_to_type.to_dict()), 201


@app.route('/task/attribute-to-type/<int:task_type_id>/<int:task_attribute_id>', methods=['DELETE'])
def delete_attribute_to_type(task_type_id, task_attribute_id):
    attribute_to_type = TaskAttributeToTaskType.query.get(
        (task_type_id, task_attribute_id))

    if attribute_to_type is None:
        abort(404)

    db_session.delete(attribute_to_type)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        return jsonify(message='Item cannot be deleted'), 409

    return '', 204


@app.route('/task/attribute-to-types')
@validate_query('attribute_to_type', 'query')
def get_attribute_to_types_list():
    query_data = request.args.to_dict()
    attribute_to_types = [attribute_to_type.to_dict()
                          for attribute_to_type in TaskAttributeToTaskType.query.filter_by(**query_data).all()]

    return jsonify(attribute_to_types), 200

@app.route('/task/attribute-to-types', methods=['POST'])
@validate_json('attribute_to_type', 'search')
def get_attribute_to_types_list_complex():
    data = request.get_json()

    attribute_to_types = [attribute_to_type.to_dict()
                for attribute_to_type in query_from_dict(TaskAttributeToTaskType, data)]

    return jsonify(attribute_to_types), 200
