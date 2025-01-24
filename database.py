# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://my_database_onrender_user:aE2Vsxgwp5rOvs00g1vQlLcyBiO5PWTV@dpg-cu8gra5ds78s73a80r2g-a.ohio-postgres.render.com/my_database_onrender"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()