from datetime import datetime
from database import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, \
    Boolean, LargeBinary
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from endpoints import app

bcrypt = Bcrypt(app)


class User(Model):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    login = Column(String(length=128), unique=True, nullable=False)
    first_name = Column(String(length=128), nullable=False)
    last_name = Column(String(length=128), nullable=False)
    password = Column(LargeBinary(60), nullable=False)
    is_creator = Column(Boolean(), nullable=False, default=False)
    is_contractor = Column(Boolean(), nullable=False, default=False)
    is_admin = Column(Boolean(), nullable=False, default=False)

    created_tasks = relationship(
        'Task', back_populates='creator', foreign_keys='Task.creator_id')
    completed_tasks = relationship(
        'Task', back_populates='contractor', foreign_keys='Task.contractor_id')

    def __init__(self, login, password, first_name, last_name,
                 is_creator=False, is_contractor=False, is_admin=False):
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.is_creator = is_creator
        self.is_contractor = is_contractor
        self.is_admin = is_admin

        self.generate_password_hash(password)

    def generate_password_hash(self, password):
        self.password = bcrypt.generate_password_hash(password, rounds=12)

    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Task(Model):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), nullable=False)
    external_identifier = Column(String(length=128), nullable=True)
    type_id = Column(Integer(), ForeignKey('task_types.id'), nullable=False)
    end_date = Column(DateTime())
    create_date = Column(DateTime(), nullable=False)

    # Foreign keys
    status_id = Column(Integer(), ForeignKey(
        'task_statuses.id'), nullable=False)
    creator_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    contractor_id = Column(Integer(), ForeignKey('users.id'), nullable=True)

    # Relationships
    status = relationship('TaskStatus', back_populates='tasks')
    type = relationship('TaskType', back_populates='tasks')
    creator = relationship(
        'User', back_populates='created_tasks', foreign_keys=[creator_id])
    contractor = relationship(
        'User', back_populates='completed_tasks', foreign_keys=[contractor_id])

    def __init__(self, name, type_id, status_id, creator_id, external_identifier=None):
        self.name = name
        self.type_id = type_id
        self.status_id = status_id
        self.creator_id = creator_id
        self.external_identifier = external_identifier
        self.create_date = datetime.today()


class TaskStatus(Model):
    __tablename__ = 'task_statuses'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    tasks = relationship('Task', back_populates='status')

    def __init__(self, name):
        self.name = name


class TaskType(Model):
    __tablename__ = 'task_types'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    # Relationships
    tasks = relationship('Task', back_populates='type')
    attributes = relationship(
        'TaskAttribute', secondary='task_attribute_to_task_type')

    def __init__(self, name):
        self.name = name


class TaskAttribute(Model):
    __tablename__ = 'task_attributes'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    # Foreign keys
    type_id = Column(Integer(), ForeignKey(
        'task_attribute_types.id'), nullable=False)

    def __init__(self, name, type_id):
        self.name = name
        self.type_id = type_id


class TaskAttributeToTaskType(Model):
    __tablename__ = 'task_attribute_to_task_type'

    task_type_id = Column(Integer(), ForeignKey(
        'task_types.id'), primary_key=True)
    task_attribute_id = Column(Integer(), ForeignKey(
        'task_attributes.id'), primary_key=True)
    sort = Column(Integer(), nullable=False, default=0)
    rules = Column(Text)

    def __init__(self, task_type_id, task_attribute_id, sort=0, rules=None):
        self.task_type_id = task_type_id
        self.task_attribute_id = task_attribute_id
        self.sort = sort
        self.rules = rules


class TaskAttributeValue(Model):
    __tablename__ = 'task_attribute_values'

    id = Column(Integer(), primary_key=True)
    value = Column(Text(), nullable=False)

    def __init__(self, value):
        self.value = value


class TaskAttributeType(Model):
    __tablename__ = 'task_attribute_types'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
