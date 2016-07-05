from create_app import app
from flask import jsonify, abort, request
from models import Task, User, TaskStatus
from database import db_session
from sqlalchemy.exc import IntegrityError, StatementError
from validation.json import validate_json
from validation.query import validate_query


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
@validate_json('user', 'update')
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()

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
    user = User.query.filter_by(id=user_id).first()

    if not user:
        abort(404)

    try:
        db_session.delete(user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='User cannot be deleteted')), 409

    db_session.delete(user)
    db_session.commit()

    return '', 204


@app.route('/users', methods=['GET'])
@validate_query('user', 'query')
def get_users_list():
    users_list = [user.to_dict()
                  for user in User.query.filter_by(**request.args.to_dict()).all()]

    return jsonify(users_list), 200


@app.route('/task/status/<int:status_id>')
def get_status(status_id):
    status = TaskStatus.query.filter_by(id=status_id).first()
    if status is None:
        abort(404)

    return jsonify(status.to_dict()), 200


@app.route('/task/status/<int:status_id>', methods=['PUT'])
@validate_json('status', 'update')
def update_status(status_id):
    status = TaskStatus.query.filter_by(id=status_id).first()

    if status is None:
        abort(404)

    data = request.get_json()
    status.update_from_dict(data)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Status name already exist')), 409

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
        return jsonify(dict(message='Status name already exist')), 409

    return jsonify(status.to_dict()), 201


@app.route('/task/status/<int:status_id>', methods=['DELETE'])
def delete_status(status_id):
    status = TaskStatus.query.filter_by(id=status_id).first()

    if status is None:
        abort(404)

    db_session.delete(status)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Status cannot be deleteted')), 409

    return '', 204


@app.route('/statuses')
@validate_query('status', 'query')
def get_statuses_list():
    statuses = [status.to_dict()
                for status in TaskStatus.query.filter_by(**request.args.to_dict()).all()]

    return jsonify(statuses), 200
