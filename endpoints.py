from create_app import app
from flask import jsonify, abort, request
from flask.json import loads as json_loads
from models import Task, User
from database import db_session
from sqlalchemy.exc import IntegrityError

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
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        abort(404)

    data = json_loads(request.data)

    try:
        user.update_from_dict(data)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify(dict(message='Login already in use')), 409

    return jsonify(user.to_dict()), 200
