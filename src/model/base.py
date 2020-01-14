from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
#engine = create_engine('postgresql://postgres:mysecretpassword@postgresdb/brian')

Session = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.drop_all(bind=engine)
