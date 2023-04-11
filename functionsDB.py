# imports

# own packages
from models import Base, Product, Store, Type_product, Contry, Currency, Rol, User, Base
from classDB import Connection

# external packages
from sqlalchemy import insert, update as Update, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os
import pandas as pd
import ast
from datetime import datetime



def create_tables()->None:
    
    """Crea las tablas con referencia al models"""
    
    connection = Connection()
    with Connection.engine.connect() as con:
        Base.metadata.create_all(Connection.engine, checkfirst=True)



def check_keys(model: str = None, keys: list | str = None, show_msm: bool = True): 
    
    """verifica que las llaves del diccionario de dado meto esten correctas"""
    
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

def create(model: str, data: list | dict = None, debug: bool = True, return_data = True) -> dict| bool | None:
    
    """Crea una nueva fila, pasandole el modelo y el diccionario a inngresar"""
    
    if debug:
        len_data = len(data)
        dict_error = []
        
        if type(data) is list:
            
            index_error = []
            
            for index, dt in enumerate(data):
                is_correct = check_keys(model = model, keys = dt.keys())
                if not(is_correct): 
                    index_error.append(index)
            
            if len(index_error) == len(data):
                print("El formato ingresado esta completamente malo verifica bien que este bien escrito el nombre de los campos")
                return False
            
            if len(index_error) >= 1:
                index_error.reverse()
                for index in index_error:
                    dict_error.append(data.pop(index))

                print(f"de {len_data}, {len(index_error)} estan malos, los cuales sus index son: {index_error}")
                print(f"del resto {len(data)} su estructura esta bien asi que se procedera a crear en la base de datos.")

                
        else: 
            is_correct = check_keys(model = model, keys = data.keys())
            if not(is_correct):
                return is_correct


    connection = Connection()
    with Connection.engine.connect() as con:
        
        try:
            connection.session.execute(insert(model), data)
            model.__msm__(data = data)
        except TypeError as e:
            model.__msm__(data = data, msm = "error")
            print(e)
                
        connection.session.commit()
    
    if debug:
    
        if len(dict_error) >= 1:
            print("Se te va a retornar los diccionarios que estan mal estructurados para que los puedas arreglas e ingresar de nuevo")
            return dict_error



def read(model: str, search : dict = None, debug = True, and_or: str = "and") -> list | dict:
    
    """Trae toda la data de la tabla o una en especifico dependiendo de los parametors que queremos que busque, para que haga esto debemos
    pasarle un diccionario con los campos que corresponden a su modelo y si estos estan bien realizara la busqueda"""
    
    if debug:
        if type(search) is dict:
            params_search = list(search.keys())

            if search != None:
                if not(check_keys(model=model, keys = params_search)):
                    print("La busqueda que esta realizando esta mal escrita o mal estructurada, intente de nuevo.")
                    return
                
        if type(search) is list:
            searchs = search
            for search in searchs: 
                params_search = list(search.keys())

                if search != None:
                    if not(check_keys(model=model, keys = params_search)):
                        print("La busqueda que esta realizando esta mal escrita o mal estructurada, intente de nuevo.")
                        return
            search = searchs
    
    connection = Connection()
    with connection.engine.connect() as con:
        
        if search == None: # si no se le astablece un paramtro de busqueda listara todos los elementos de la tabla y retornara un dataFrame
            data = connection.session.execute(text(f"SELECT * FROM {model.__tablename__}")).fetchall()
            data_list = []
            for index in range(0, len(data)):
                data_dict = {key:value for key,value in zip(model.__column__, data[index])}
                data_list.append(data_dict)
            return pd.DataFrame(data_list)
        
        else:
            
            querys = []
            print()
            if type(search) is dict:
                params_search = list(search.keys())
                params_value = list(search.values())
                query = f"SELECT * FROM {model.__tablename__} WHERE "
                
                if len(params_search) >= 2:
                    for search, value in zip(params_search, params_value):
                        if type(value) is str: query+= f"{and_or} {search} = '{value}'"
                        elif type(value) is int or  type(value) is bool: query+= f"{and_or} {search} = {value}"
                        querys.append(query)
                else:
                    if type(params_value[0]) is str: query+= f" {params_search[0]} = '{params_value[0]}'"
                    elif type(params_value[0]) is int or type(params_value[0]) is bool: query+= f" {params_search[0]} = {params_value[0]}"
                    querys.append(query)
                    
            elif type(search) is list:
                searchs = search
                for search in searchs:
                    if type(search) is dict:
                        params_search = list(search.keys())
                        params_value = list(search.values())
                        query = f"SELECT * FROM {model.__tablename__} WHERE "
                        
                        if len(params_search) >= 2:
                            for search, value in zip(params_search, params_value):
                                if type(value) is str: query+= f"{and_or} {search} = '{value}'"
                                elif type(value) is int or  type(value) is bool: query+= f"{and_or} {search} = {value}"
                                querys.append(query)
                        else:
                            if type(params_value[0]) is str: query+= f" {params_search[0]} = '{params_value[0]}'"
                            elif type(params_value[0]) is int or type(params_value[0]) is bool: query+= f" {params_search[0]} = {params_value[0]}"
                            querys.append(query)
            list_search = []
            if len(querys) >= 2:
                
                for query in querys:
                    datos = connection.session.execute(text(query)).fetchall()
                    
                    if len(datos) == 0:
                        print("Lo que esta buscando no existe o esta mal escrito, intente de nuevo")
                        list_search.append(False)
                    else:
                        for data in datos:
                            data_dict = {key:value for key,value in zip(model.__column__, data)}
                            list_search.append(data_dict)
                            
                return list_search
            
            elif len(querys) == 1:
                datos = connection.session.execute(text(query)).fetchall()
                if len(datos) == 0:
                    print("Lo que esta buscando no existe o esta mal escrito, intente de nuevo")
                    return False
                elif len(datos) >= 2:
                    for data in datos:
                        data_dict = {key:value for key,value in zip(model.__column__, data)}
                        list_search.append(data_dict)
                            
                    return list_search
                elif len(datos) >= 1:
                    data_dict = {key:value for key,value in zip(model.__column__, datos[0])}
                    return data_dict



def update(model: str, param: dict | list):
    
    """Realiza uno o varios paramtros dependiendo del modelo y el diccionario que ingresemos"""
    
    if not(check_keys(model=model, keys=list(param.keys()))):
        print("La peticion ingresada, esta mal escrita, o no existe el paramtro al que se esta consultando.")
        return
    
    model_id, model_unique = model.__column__[0], model.__unique__
    
    conection = Connection()
    with conection.engine.connect() as con:
        
        if type(param) is dict:
            keys_param = list(param.keys())
            
            if model_id in keys_param:
                conection.session.execute(Update(model), param)
                conection.session.commit()
                print("Actualizado")
                
            elif model_unique in keys_param:
                data = read(model=model, search={model_unique:param[model_unique]})
                param[model_id] = data[0][model_id]
                conection.session.execute(Update(model), param)
                conection.session.commit()
                print("Actualizado")
                
        elif type(param) is list:
            
            params = param
            for param in params:
                if model_id in keys_param:
                    conection.session.execute(Update(model), param)
                    conection.session.commit()
                    print("Actualizado")
                    
                elif model_unique in keys_param:
                    data = read(model=model, search={model_unique:param[model_unique]})
                    param[model_id] = data[0][model_id]
                    conection.session.execute(Update(model), param)
                    conection.session.commit()
                    print("Actualizado")
    
    
    
def load_collector(json_file: str = None) -> None: # falta verificar que los productoos ya existan y si es asi que lo actualize 
    
    
    """Acepta como parametro la direcion en carpeta de un json lo procesa acorde al modelo de product he ingresa estos datos en su tabla"""
    
    dataFrame = pd.read_json(json_file)
    connection = Connection()
    
    
    # contry
    dict_contry = {}
    contrys = dataFrame["contry"]
    last_contry = ""
    for index, _ in enumerate(contrys):
        
        if contrys[index] != last_contry:
            contry = read(Contry, {"contry_name":contrys[index]}, debug=False)
            if not(contry):
                create(Contry, {"contry_name":contrys[index]}, debug=False)
                contry = read(Contry, {"contry_name":contrys[index]}, debug=False)
                dict_contry[contry["contry_name"]] = contry["contry_id"]
                last_contry = contry["contry_name"]
            else:
                dict_contry[contry["contry_name"]] = contry["contry_id"]
                last_contry = contry["contry_name"]
        else:
            continue
    
    
    
    # product
    dict_store = {}
    stores = dataFrame["store_name"]
    last_store = ""
    for index, _ in enumerate(stores):
        if stores[index] != last_store:
            store = read(Store, {"store_name":stores[index]}, debug=False)
            if not(store):
                create(Store, {"contry_id":dict_contry[dataFrame["contry"][index]] ,"store_name":stores[index], "link_store": dataFrame["parent_website"][index], "load_collector_num":1, "last_modification_day":str(datetime.now())[0:10]}, debug=False)
                store = read(Store, {"store_name":stores[index]}, debug=False)
                dict_store[store["store_name"]] = store["store_id"]
                last_store = store["store_name"]
            else:
                dict_store[store["store_name"]] = store["store_id"]
                last_store = store["store_name"]
        else:
            continue
        
    verify_stores = list(dict_store.keys())
    with connection.engine.connect() as con:
        for store_name in verify_stores:
            store = read(Store, {"store_name":store_name}, debug=False)
            time_now = str(datetime.now())[0:10]
            if time_now != store["last_modification_day"]:
                store["last_modification_day"] = int(store["last_modification_day"]) + 1
                store["last_modification_day"] = time_now
                connection.session.execute(Update, store)
                connection.session.commit()



    # product_type
    dict_product_type = {}
    product_types = dataFrame["product_type"]
    last_product_type = ""
    for index, _ in enumerate(product_types):
        if product_types[index] != last_product_type:
            product_type = read(Type_product,  {"product_type_name":product_types[index]}, debug=False)
            if not(product_type):
                create(Type_product, {"product_type_name":product_types[index]}, debug=False)
                product_type = read(Type_product,  {"product_type_name":product_types[index]},  debug=False)
                dict_product_type[product_type["product_type_name"]] =  product_type["product_type_id"]
                last_product_type = product_type["product_type_name"]
            else: 
                dict_product_type[product_type["product_type_name"]] =  product_type["product_type_id"]
                last_product_type = product_type["product_type_name"]
        else:
            continue
    
    
    
    # price
    dict_currency = {}
    currencys= dataFrame["price"]
    last_currency = ""
    for index, _ in enumerate(currencys):
        if currencys[index]["currency"] != last_currency:
            currency = read(Currency, {"currency_name": currencys[index]["currency"]}, debug=False)
            if not(currency):
                create(Currency, {"currency_name": currencys[index]["currency"], "symbol":currencys[index]["symbol"]}, debug=False)
                currency = read(Currency, {"currency_name": currencys[index]["currency"]}, debug=False)
                dict_currency[currency["currency_name"]] = currency["currency_id"]
                last_currency = currency["currency_name"]
            else:
                dict_currency[currency["currency_name"]] = currency["currency_id"]
                last_currency = currency["currency_name"]
        else:
            continue
    
    collectors = []
    for index in range(0, len(dataFrame)):

        
        data = {
        "store_id": dict_store[dataFrame["store_name"][index]],
        "product_type_id": dict_product_type[dataFrame["product_type"][index]],
        "currency_id": dict_currency[dataFrame["price"][index]["currency"]],
        "link": dataFrame['link'][index],
        "title": dataFrame['title'][index], 
        "description": dataFrame['description'][index], 
        "product_brand": dataFrame['product_brand'][index], 
        "img_urls": str(dataFrame['img_urls'][index]),
        "img_direction_folder":str(dataFrame['img_direction_folder'][index]), 
        "price": dataFrame['price'][index]["value"],
        "discount_price": dataFrame['discount_price'][index]["value"],
        "has_discount":(dataFrame["price"][index]["value"] - dataFrame["discount_price"][index]["value"]) != 0,
        "characteristics": dataFrame['characteristics'][index]
        }

        collectors.append(data)
        
    create(Product, collectors, debug=False)

load_collector("pruebas/ejemplo_load_collector.json")