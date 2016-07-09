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


@app.route('/task/attribute/<int:attribute_id>')
def get_attribute(attribute_id):
    attribute = TaskAttribute.query.get(attribute_id)

    if attribute is None:
        abort(404)

    return jsonify(attribute.to_dict()), 200


@app.route('/task/attribute/<int:attribute_id>', methods=['PUT'])
@validate_json('attribute', 'update')
def update_attribute(attribute_id):
    attribute = TaskAttribute.query.get(attribute_id)

    if attribute is None:
        abort(404)

    data = request.get_json()
    attribute.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        return jsonify(message=str(e)), 409

    return jsonify(attribute.to_dict()), 200


@app.route('/task/attribute', methods=['POST'])
@validate_json('attribute', 'create')
def create_attribute():
    data = request.get_json()
    attribute = TaskAttribute.create_from_dict(data)

    db_session.add(attribute)

    try:
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        return jsonify(message=str(e)), 409

    return jsonify(attribute.to_dict()), 201


@app.route('/task/attribute/<int:attribute_id>', methods=['DELETE'])
def delete_attribute(attribute_id):
    attribute = TaskAttribute.query.get(attribute_id)

    if attribute is None:
        abort(404)

    db_session.delete(attribute)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        return jsonify(message='Attribute cannot be deleted'), 409

    return '', 204


@app.route('/task/attributes')
@validate_query('attribute', 'query')
def get_attributes_list():
    query_data = request.args.to_dict()
    attributes = [attribute.to_dict()
                  for attribute in TaskAttribute.query.filter_by(**query_data).all()]

    return jsonify(attributes), 200


@app.route('/task/attributes', methods=['POST'])
@validate_json('attribute', 'search')
def get_attribute_list_complex():
    data = request.get_json()

    attributes = [attribute.to_dict()
                       for attribute in query_from_dict(TaskAttribute, data)]

    return jsonify(attributes), 200
