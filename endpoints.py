from create_app import app
from flask import jsonify, abort, request
from models import Task, User
from database import db_session
from sqlalchemy.exc import IntegrityError, StatementError
from validation.json import validate_json


@app.route('/')
def index():
    tasks = []

    for task in Task.query.all():
        tasks.append(task.to_dict())

    return jsonify(tasks), 200


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
