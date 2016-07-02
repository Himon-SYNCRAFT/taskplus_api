from database import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship


class User(Model):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    created_tasks = relationship('Task', back_populates='creator')
    completed_tasks = relationship('Task', back_populates='contractor')


class Task(Model):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), nullable=False)
    external_identifier = Column(String(length=128))
    type_id = Column(Integer(), ForeignKey('task_types.id'), nullable=False)
    status_id = Column(Integer(), ForeignKey(
        'task_statuses.id'), nullable=False)
    creator_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    contractor_id = Column(Integer(), ForeignKey('users.id'), nullable=True)
    create_date = Column(DateTime(), nullable=False)
    end_date = Column(DateTime())

    status = relationship('TaskStatus', back_populates='tasks')
    type = relationship('TaskType', back_populates='tasks')
    creator = relationship(
        'User', back_populates='created_tasks', foreign_keys='creator_id')
    contractor = relationship(
        'User', back_populates='completed_tasks', foreign_keys='contractor_id')


class TaskStatus(Model):
    __tablename__ = 'task_statuses'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    tasks = relationship('Task', back_populates='status')


class TaskType(Model):
    __tablename__ = 'task_types'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    tasks = relationship('Task', back_populates='type')


class TaskAttribute(Model):
    __tablename__ = 'task_attributes'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)
    type_id = Column(Integer(), ForeignKey(
        'task_attribute_types.id'), nullable=False)


class TaskAttributeValue(Model):
    __tablename__ = 'task_attribute_values'

    id = Column(Integer(), primary_key=True)
    value = Column(Text(), nullable=False)


class TaskAttributeType(Model):
    __tablename__ = 'task_attribute_type'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)
