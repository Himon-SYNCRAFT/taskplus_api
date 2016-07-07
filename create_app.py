from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
import click
import unittest

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

bcrypt = Bcrypt(app)


@app.cli.command()
@click.argument('data', nargs=-1)
def test(data):
    case_name = 'test_' + data[0] + '.Test' + data[0].title().replace('_', '')

    if len(data) > 1:
        test_name = data[1]
    else:
        test_name = ''

    tests_path = case_name

    if test_name:
        tests_path += '.' + test_name

    tests = unittest.TestLoader().loadTestsFromName('tests.' + tests_path)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(tests)
