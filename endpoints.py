from create_app import app
from flask import jsonify
from models import Task, User


@app.route('/')
def index():
    tasks = []

    for task in Task.query.all():
        tasks.append(task.to_dict())

    return jsonify(tasks), 200


@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.to_dict()), 200
