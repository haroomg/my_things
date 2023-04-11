from models import Store, Contry, Currency, Rol, Product, Type_product, User, Match_product, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



class Connection():
    
    url = f"sqlite:///matcher_db.sqlite"
    engine = create_engine(url) 
    Session  = sessionmaker(bind= engine)
    session =  Session()
