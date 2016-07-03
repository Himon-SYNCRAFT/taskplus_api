from flask_testing import TestCase
from create_app import app
from create_db import create_db
from database import db_session, create_engine, Model


class Base(TestCase):

    def create_app(self):
        app.config.from_object('settings.TestConfig')
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        return app

    def setUp(self):
        db_session.configure(bind=self.engine)
        db_session.remove()

        create_db(db_session)

    def tearDown(self):
        db_session.remove()
        Model.metadata.drop_all(self.engine)
