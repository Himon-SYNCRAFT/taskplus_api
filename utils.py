from database import db_session


def query_from_dict(Class, data):
    if not isinstance(data, dict):
        raise TypeError('Second parameter should be instance of dict')
    if not hasattr(Class, 'query'):
        raise TypeError

    query = Class.query

    if not hasattr(query, 'all') or not hasattr(query, 'filter'):
        raise TypeError('Class is not instance of sqlalchemy model')

    for key, item in data.items():
        if not isinstance(item, dict):
            raise TypeError(
                'Bad formated data. Each item in data should have value of dict=(value='', operator='')')

        if 'operator' in item:
            operator = item['operator']
        else:
            operator = '='

        value = item['value']

        if operator == '!=':
            query = query.filter(getattr(Class, key) != value)
        elif operator == '>':
            query = query.filter(getattr(Class, key) > value)
        elif operator == '<':
            query = query.filter(getattr(Class, key) < value)
        elif operator == '>=':
            query = query.filter(getattr(Class, key) >= value)
        elif operator == '<=':
            query = query.filter(getattr(Class, key) <= value)
        else:
            query = query.filter(getattr(Class, key) == value)

    rv = query.all()

    return rv
