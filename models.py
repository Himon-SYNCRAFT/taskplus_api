from datetime import datetime
from database import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, \
    Boolean, LargeBinary
from sqlalchemy.orm import relationship
from create_app import app, bcrypt
from exceptions import ValidationError


class User(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
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

    def _get_fields(self):
        fields = ['login', 'first_name', 'last_name',
                  'is_creator', 'is_contractor', 'is_admin']

        return fields

    def generate_password_hash(self, password):
        self.password = bcrypt.generate_password_hash(password, rounds=12)

    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return dict(
            id=self.id,
            login=self.login,
            first_name=self.first_name,
            last_name=self.last_name,
            is_creator=self.is_creator,
            is_contractor=self.is_contractor,
            is_admin=self.is_admin
        )

    def update_from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError

        for field in self._get_fields():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def create_from_dict(data):
        if not isinstance(data, dict):
            raise TypeError

        user = User(login='tmp', password='tmp',
                    first_name='tmp', last_name='tmp')

        for field in user._get_fields():
            try:
                setattr(user, field, data[field])
            except KeyError as e:
                raise ValidationError('Invalid class: missing ' + e.args[0])

        try:
            user.generate_password_hash(data['password'])
        except KeyError as e:
            raise ValidationError('Invalid class: missing ' + e.args[0])

        return user

    def __str__(self):
        return str(self.to_dict())


class Task(Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=128), nullable=False)
    external_identifier = Column(String(length=128), nullable=True)
    type_id = Column(Integer, ForeignKey('task_types.id'), nullable=False)
    end_date = Column(DateTime(timezone=True))
    create_date = Column(DateTime(timezone=True), nullable=False)

    # Foreign keys
    status_id = Column(Integer, ForeignKey(
        'task_statuses.id'), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contractor_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Relationships
    status = relationship('TaskStatus', back_populates='tasks')
    type = relationship('TaskType', back_populates='tasks')
    creator = relationship(
        'User', back_populates='created_tasks', foreign_keys=[creator_id])
    contractor = relationship(
        'User', back_populates='completed_tasks', foreign_keys=[contractor_id])
    content = relationship('TaskAttributeValue')

    def __init__(self, name, type_id, status_id, creator_id, external_identifier=None):
        self.name = name
        self.type_id = type_id
        self.status_id = status_id
        self.creator_id = creator_id
        self.external_identifier = external_identifier
        self.create_date = datetime.today()

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            external_identifier=self.external_identifier,
            type_id=self.type_id,
            end_date=self.end_date,
            create_date=self.create_date,
            status_id=self.status_id,
            creator_id=self.creator_id,
            contractor_id=self.contractor_id
        )


class TaskStatus(Model):
    __tablename__ = 'task_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    tasks = relationship('Task', back_populates='status')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return dict(id=self.id, name=self.name)

    def _get_fields(self):
        fields = ['name']

        return fields

    def update_from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError

        for field in self._get_fields():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def create_from_dict(data):
        if not isinstance(data, dict):
            raise TypeError

        status = TaskStatus(name='tmp')

        for field in status._get_fields():
            try:
                setattr(status, field, data[field])
            except KeyError as e:
                raise ValidationError('Invalid class: missing ' + e.args[0])

        return status


class TaskType(Model):
    __tablename__ = 'task_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    # Relationships
    tasks = relationship('Task', back_populates='type')
    attributes = relationship(
        'TaskAttribute', secondary='task_attribute_to_task_type')

    def __init__(self, name):
        self.name = name

    def _get_fields(self):
        fields = ['name']

        return fields

    def update_from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError

        for field in self._get_fields():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def create_from_dict(data):
        if not isinstance(data, dict):
            raise TypeError

        task_type = TaskType(name='tmp')

        for field in task_type._get_fields():
            try:
                setattr(task_type, field, data[field])
            except KeyError as e:
                raise ValidationError('Invalid class: missing ' + e.args[0])

        return task_type

    def to_dict(self):
        return dict(id=self.id, name=self.name)


class TaskAttribute(Model):
    __tablename__ = 'task_attributes'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    # Foreign keys
    type_id = Column(Integer, ForeignKey(
        'task_attribute_types.id'), nullable=False)

    def __init__(self, name, type_id):
        self.name = name
        self.type_id = type_id

    def _get_fields(self):
        fields = ['name', 'type_id']

        return fields

    def update_from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError

        for field in self._get_fields():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def create_from_dict(data):
        if not isinstance(data, dict):
            raise TypeError

        attribute = TaskAttribute(name='tmp', type_id=1)

        for field in attribute._get_fields():
            try:
                setattr(attribute, field, data[field])
            except KeyError as e:
                raise ValidationError('Invalid class: missing ' + e.args[0])

        return attribute

    def to_dict(self):
        return dict(id=self.id, name=self.name, type_id=self.type_id)


class TaskAttributeToTaskType(Model):
    __tablename__ = 'task_attribute_to_task_type'

    task_type_id = Column(Integer, ForeignKey(
        'task_types.id'), primary_key=True, nullable=False)
    task_attribute_id = Column(Integer, ForeignKey(
        'task_attributes.id'), primary_key=True, nullable=False)
    sort = Column(Integer, nullable=False, default=0)
    rules = Column(Text)

    def __init__(self, task_type_id, task_attribute_id, sort=0, rules=None):
        self.task_type_id = task_type_id
        self.task_attribute_id = task_attribute_id
        self.sort = sort
        self.rules = rules


class TaskAttributeValue(Model):
    __tablename__ = 'task_attribute_values'

    value = Column(Text, nullable=False)

    # Foreign keys
    task_id = Column(Integer, ForeignKey('tasks.id'),
                     primary_key=True, nullable=False)
    task_attribute_id = Column(Integer, ForeignKey(
        'task_attributes.id'), primary_key=True, nullable=False)

    def __init__(self, task_id, task_attribute_id, value):
        self.value = value
        self.task_id = task_id
        self.task_attribute_id = task_attribute_id

    def to_dict(self):
        return dict(
            value=self.value,
            task_id=self.task_id,
            task_attribute_id=self.task_attribute_id
        )

    def _get_fields(self):
        fields = ['value', 'task_id', 'task_attribute_id']

        return fields

    def update_from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError

        for field in self._get_fields():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def create_from_dict(data):
        if not isinstance(data, dict):
            raise TypeError

        value = TaskAttributeValue(value='tmp', task_id=1, task_attribute_id=1)

        for field in value._get_fields():
            try:
                setattr(value, field, data[field])
            except KeyError as e:
                raise ValidationError('Invalid class: missing ' + e.args[0])

        return value


class TaskAttributeType(Model):
    __tablename__ = 'task_attribute_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def _get_fields(self):
        fields = ['name']

        return fields

    def update_from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError

        for field in self._get_fields():
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def create_from_dict(data):
        if not isinstance(data, dict):
            raise TypeError

        attribute_type = TaskAttributeType(name='tmp')

        for field in attribute_type._get_fields():
            try:
                setattr(attribute_type, field, data[field])
            except KeyError as e:
                raise ValidationError('Invalid class: missing ' + e.args[0])

        return attribute_type

    def to_dict(self):
        return dict(id=self.id, name=self.name)
