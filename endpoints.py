from create_app import app
from flask import jsonify, abort, request
from models import Task, User
from database import db_session
from sqlalchemy.exc import IntegrityError, StatementError
from validation.json import validate_json


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
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
