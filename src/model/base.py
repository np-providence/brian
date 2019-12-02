from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:mysecretpassword@postgresdb:5432/brian')
Session = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.drop_all(bind=engine)
