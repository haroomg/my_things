from models import Store, Contry, Currency, Rol, Product, Type_product, User, Match_product, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



class Connection():
    
    url = f"sqlite:///matcher_db.sqlite"
    engine = create_engine(url) 
    Session  = sessionmaker(bind= engine)
    session =  Session()



def create_tables()->None:
    
    Connection = Connection()
    with Connection.engine.connect() as con:
        Base.metadata.create_all(Connection.engine, checkfirst=True)



def check_keys(model: str = None, keys: list | str = None, show_msm: bool = True):
    
    if type(keys) is str : keys = list(keys)
    
    columns_name = model.__column__
    error_names = []
    
    for key in keys:
        if key not in columns_name:
            error_names.append(key)
    
    if len(error_names) >= 1:
        if show_msm:
            print(f"Hay {len(error_names)} que estan mal escritos.")
            for name in error_names:
                print(f"El campo '{name}' esta mal escrito.")
        return False
    else:
        if show_msm:
            print("Todas las llaves estas bien escritas.")
        return True