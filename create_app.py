from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
import click
import unittest

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

bcrypt = Bcrypt(app)


@app.cli.command()
@click.option('-n', default=None)
def test(n):
    case_name = n

    if case_name is not None:
        tests = unittest.TestLoader().discover(
            'tests', pattern='test*' + case_name + '.py')
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
