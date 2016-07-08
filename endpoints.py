from create_app import app
from flask import jsonify, abort, request
from models import Task, User, TaskStatus, TaskType, TaskAttribute, \
    TaskAttributeType, TaskAttributeValue, TaskAttributeToTaskType
from database import db_session
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm.exc import FlushError
from validation.json import validate_json
from validation.query import validate_query


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
@validate_json('user', 'update')
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        abort(404)

    data = request.get_json()

    try:
        user.update_from_dict(data)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Login already in use')), 409

    return jsonify(user.to_dict()), 200


@app.route('/user', methods=['POST'])
@validate_json('user', 'create')
def create_user():
    data = request.get_json()

    try:
        user = User.create_from_dict(data)
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Login already in use')), 409

    return jsonify(user.to_dict()), 201


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        abort(404)

    db_session.delete(user)

    try:

        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='User cannot be deleted')), 409

    return '', 204


@app.route('/users', methods=['GET'])
@validate_query('user', 'query')
def get_users_list():
    users_list = [user.to_dict()
                  for user in User.query.filter_by(**request.args.to_dict()).all()]

    return jsonify(users_list), 200


@app.route('/task/status/<int:status_id>')
def get_status(status_id):
    status = TaskStatus.query.get(status_id)
    if status is None:
        abort(404)

    return jsonify(status.to_dict()), 200


@app.route('/task/status/<int:status_id>', methods=['PUT'])
@validate_json('status', 'update')
def update_status(status_id):
    status = TaskStatus.query.get(status_id)

    if status is None:
        abort(404)

    data = request.get_json()
    status.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Status name must be unique.')), 409

    return jsonify(status.to_dict())


@app.route('/task/status', methods=['POST'])
@validate_json('status', 'create')
def create_status():
    data = request.get_json()
    status = TaskStatus.create_from_dict(data)

    db_session.add(status)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Status name must be unique.')), 409

    return jsonify(status.to_dict()), 201


@app.route('/task/status/<int:status_id>', methods=['DELETE'])
def delete_status(status_id):
    status = TaskStatus.query.get(status_id)

    if status is None:
        abort(404)

    db_session.delete(status)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Status cannot be deleted')), 409

    return '', 204


@app.route('/task/statuses')
@validate_query('status', 'query')
def get_statuses_list():
    statuses = [status.to_dict()
                for status in TaskStatus.query.filter_by(**request.args.to_dict()).all()]

    return jsonify(statuses), 200


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
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Attribute name must be unique.'), 409

    return jsonify(attribute.to_dict()), 200


@app.route('/task/attribute', methods=['POST'])
@validate_json('attribute', 'create')
def create_attribute():
    data = request.get_json()
    attribute = TaskAttribute.create_from_dict(data)

    db_session.add(attribute)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Attribute name must be unique.'), 409

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


@app.route('/task/attribute/value/<int:task_id>/<int:task_attribute_id>')
def get_attribute_value(task_id, task_attribute_id):
    attribute_value = TaskAttributeValue.query.get((task_id, task_attribute_id))

    if attribute_value is None:
        abort(404)

    return jsonify(attribute_value.to_dict()), 200


@app.route('/task/attribute/value/<int:task_id>/<int:task_attribute_id>', methods=['PUT'])
@validate_json('attribute_value', 'update')
def update_attribute_value(task_id, task_attribute_id):
    attribute_value = TaskAttributeValue.query.get((task_id, task_attribute_id))

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
    attribute_value = TaskAttributeValue.query.get((task_id, task_attribute_id))

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
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Attribute already exist for this task type.'), 409

    return jsonify(attribute_to_type.to_dict()), 200


@app.route('/task/attribute-to-type', methods=['POST'])
@validate_json('attribute_to_type', 'create')
def create_attribute_to_type():
    data = request.get_json()
    attribute_to_type = TaskAttributeToTaskType.create_from_dict(data)

    db_session.add(attribute_to_type)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(message='Attribute already exist for this task type.'), 409
    except FlushError:
        db_session.rollback()
        return jsonify(message='Attribute already exist for this task type.'), 409

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
