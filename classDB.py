from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Conection():
    
    url = f"sqlite:///matcher_db.sqlite"
    engine = create_engine(url) 
    Session  = sessionmaker(bind= engine)
    Session =  Session()