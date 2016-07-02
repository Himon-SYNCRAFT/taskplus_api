from database import db_session, Model
import models

def create_db():

    Model.metadata.reflect()
    Model.metadata.drop_all()
    Model.metadata.create_all()

if __name__ == '__main__':
    create_db()
