from sqlalchemy import create_engine, MetaData

engine = create_engine("sqlite:///students.db", echo=True)

metadata = MetaData()