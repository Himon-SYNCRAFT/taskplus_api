from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from endpoints import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db_session = scoped_session(sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False
))


Model = declarative_base(bind=engine)
Model.query = db_session.query_property()
