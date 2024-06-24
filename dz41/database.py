from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
database_url = os.getenv("URL")
engine = create_engine(url=database_url, echo=True)
Session = sessionmaker(bind=engine)