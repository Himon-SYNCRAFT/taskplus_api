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


@app.route('/users', methods=['POST'])
@validate_json('user', 'search')
def get_users_list_complex():
    data = request.get_json()

    users_list = [user.to_dict()
                  for user in query_from_dict(User, data)]

    return jsonify(users_list), 200
