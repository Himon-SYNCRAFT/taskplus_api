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


@app.route('/task/attribute/type/<int:attribute_type_id>')
def get_attribute_type(attribute_type_id):
    attribute_type = TaskAttributeType.query.get(attribute_type_id)

    if attribute_type is None:
        abort(404)

    return jsonify(attribute_type.to_dict()), 200


@app.route('/task/attribute/type/<int:attribute_type_id>', methods=['PUT'])
@validate_json('attribute_type', 'update')
def update_attribute_type(attribute_type_id):
    attribute_type = TaskAttributeType.query.get(attribute_type_id)

    if attribute_type is None:
        abort(404)

    data = request.get_json()
    attribute_type.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Type name must be unique.'), 409

    return jsonify(attribute_type.to_dict()), 200


@app.route('/task/attribute/type', methods=['POST'])
@validate_json('attribute_type', 'create')
def create_attribute_type():
    data = request.get_json()
    attribute_type = TaskAttributeType.create_from_dict(data)

    db_session.add(attribute_type)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Type name must be unique.'), 409

    return jsonify(attribute_type.to_dict()), 201


@app.route('/task/attribute/type/<int:attribute_type_id>', methods=['DELETE'])
def delete_attribute_type(attribute_type_id):
    attribute_type = TaskAttributeType.query.get(attribute_type_id)

    if attribute_type is None:
        abort(404)

    db_session.delete(attribute_type)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        return jsonify(message='Type cannot be deleted'), 409

    return '', 204


@app.route('/task/attribute/types')
@validate_query('attribute_type', 'query')
def get_attribute_types_list():
    query_data = request.args.to_dict()
    attribute_types = [attribute_type.to_dict()
                       for attribute_type in TaskAttributeType.query.filter_by(**query_data).all()]

    return jsonify(attribute_types), 200


@app.route('/task/attribute/types', methods=['POST'])
@validate_json('attribute_type', 'search')
def get_attribute_types_list_complex():
    data = request.get_json()

    attribute_types = [attribute_type.to_dict()
                       for attribute_type in query_from_dict(TaskAttributeType, data)]

    return jsonify(attribute_types), 200
