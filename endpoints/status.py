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


@app.route('/task/statuses', methods=['POST'])
@validate_json('status', 'search')
def get_statuses_list_complex():
    data = request.get_json()

    statuses = [status.to_dict()
                for status in query_from_dict(TaskStatus, data)]

    return jsonify(statuses), 200
