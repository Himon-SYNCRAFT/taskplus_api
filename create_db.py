from database import Model
import models


def create_db(db_session=None):

    if db_session is None:
        from database import db_session

    Model.metadata.reflect(db_session.bind)
    Model.metadata.drop_all(db_session.bind)
    Model.metadata.create_all(db_session.bind)

    statuses = [
        models.TaskStatus(name='Nowe'),
        models.TaskStatus(name='W trakcie realizacji'),
        models.TaskStatus(name='Zrealizowane'),
        models.TaskStatus(name='Anulowane')
    ]

    for item in statuses:
        db_session.add(item)

    db_session.commit()

    task_types = [
        models.TaskType(name='Zmiana ceny'),
        models.TaskType(name='Dodaj nowy produkt'),
    ]

    for item in task_types:
        db_session.add(item)

    db_session.commit()

    users = [
        models.User('admin', 'admin', 'Daniel', 'Zawłocki', True, True, True),
        models.User('danzaw', 'danzaw', 'Daniel',
                    'Zawłocki', True, True, False),
        models.User('przoci', 'przoci', 'Przemek',
                    'Ociepa', False, True, False)
    ]

    for item in users:
        db_session.add(item)

    db_session.commit()

    task_attribute_types = [
        models.TaskAttributeType(name='string'),
        models.TaskAttributeType(name='int'),
        models.TaskAttributeType(name='float'),
        models.TaskAttributeType(name='list'),
        models.TaskAttributeType(name='json'),
    ]

    for item in task_attribute_types:
        db_session.add(item)

    db_session.commit()

    task_attributes = [
        models.TaskAttribute(name='Nazwa produktu', type_id=1),
        models.TaskAttribute(name='Cena', type_id=3),
        models.TaskAttribute(name='Opis', type_id=1),
    ]

    for item in task_attributes:
        db_session.add(item)

    db_session.commit()

    task_attribute_to_task_types = [
        models.TaskAttributeToTaskType(1, 1),
        models.TaskAttributeToTaskType(2, 1),
        models.TaskAttributeToTaskType(1, 2),
        models.TaskAttributeToTaskType(2, 2),
        models.TaskAttributeToTaskType(2, 3)
    ]

    for item in task_attribute_to_task_types:
        db_session.add(item)

    db_session.commit()

    tasks = [
        models.Task(name='Zmiana ceny czegos tam',
                    type_id=1, status_id=1, creator_id=2),
        models.Task(name='Dodaj cos tam', type_id=2,
                    status_id=1, creator_id=2),
    ]

    for item in tasks:
        db_session.add(item)

    db_session.commit()

    tasks_content = [
        models.TaskAttributeValue(1, 1, 'Laptop Asus'),
        models.TaskAttributeValue(1, 2, 10.00),
        models.TaskAttributeValue(2, 1, 'Laptop Asus2'),
        models.TaskAttributeValue(2, 2, 110.00),
        models.TaskAttributeValue(2, 3, 'Bardzo fajny laptop')
    ]

    for item in tasks_content:
        db_session.add(item)

    db_session.commit()


if __name__ == '__main__':
    create_db()
