from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
#engine = create_engine('postgresql://postgres:mysecretpassword@172.17.0.2:5432/postgres')
Session = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.drop_all(bind=engine)
