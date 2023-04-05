from sqlalchemy import Column, Integer, Float, Boolean, String, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()



class Product(Base):
    __tablename__ = "products"
    __column__ = [
        "product_id", "store_id_fk", "product_type_id_fk", "currency_id_fk", "link", "title",
        "description", "product_brand", "img_urls", "img_direction_folder", "price", "discount_price",
        "has_discount", "characteristics"
        ]
    __column_db__ = [
        "product_id", "store_id", "product_type_id", "currency_id", "link_produc", "title",
        "description", "product_brand", "img_urls", "img_direction_folder", "price", "discount_price",
        "has_discount", "characteristics"
        ]

    def __str_create__(data, error=True):
        if error:
            print(f"Producto creado exitosamente")
        else:
            print(f"error al crear un nuevo producto")

    product_id = Column("product_id", Integer, primary_key=True) # id del producto
    store_id_fk = Column("store_id_fk", Integer(), ForeignKey("stores.store_id")) # id de la tienda y su link
    product_type_id_fk = Column("product_type_id_fk", String(256), ForeignKey("type_products.product_type_id")) # id del tipo de producto al que corresponde
    currency_id_fk = Column("currency_id_fk", ForeignKey("currencies.currency_id"))
    
    link_produc = Column("link_produc", Text(), unique=True) # link del producto / este es un campo unico
    title = Column("title", Text()) # titulo del producto, con este es que se va a realizar la busqueda
    description = Column("description", Text()) #descripcion del producto
    product_brand = Column("product_brand", String(256)) # nombre de la marca del producto 
    
    img_urls = Column("img_urls", JSON()) # urls de las imagenes del producto
    img_direction_folder = Column("img_direction_folder", JSON()) # Nombre y direncion en carpeta donde se encuentra la imagen descargada
    
    price = Column("price", Float()) # precio
    discount_price = Column("discount_price", Float()) # precio del producto con descuento
    has_discount = Column("has_discount", Boolean()) # valor buleano para decir si tiene un producto
    characteristics = Column("characteristics", JSON()) # json con las carcateristicas del producto



class Type_product(Base):
    __tablename__ = "type_products"
    __column__ = ["product_type_id", "product_type_name"]
    __column_db__ = __column__
    
    def __str_create__(data, error=True):
        if error:
            print(f"Agregando '{data['product_type_name']}'.")
        else:
            print(f"Error, '{data['product_type_name']}' ya existe y no pueden existir dos product_type_name iguales.")
    
    product_type_id = Column("product_type_id", Integer(), primary_key=True) # id tipo de producto
    product_type_name = Column("product_type_name", String(50)) # nombre del tipo de producto



class Currency(Base):
    __tablename__ = "currencies"
    __column__ = ["currency_id", "currency_name", "symbol"]
    __column_db__ = __column__
    
    def __str_create__(data, error=True):
        if error:
            print(f"Agregando '{data['currency_name']}'.")
        else:
            print(f"Error, '{data['currency_name']}' ya existe y no pueden existir dos currency_name iguales.")
    
    currency_id = Column("currency_id", Integer(), primary_key=True) # id de la diviza
    currency_name = Column("currency_name", String(50)) # nombre de la diviza
    symbol = Column("symbol", String(20))



class Contry(Base):

    __tablename__ = "contries"
    __column__ = ["contry_id", "contry_name"]
    __column_db__ = __column__
    
    def __str_create__(data, error=True):
        if error:
            print(f"Agregando el pais '{data['contry_name']}'.")
        else:
            print(f"Error, el pais '{data['contry_name']}' ya existe y no pueden existir dos contry_name iguales.")
    
    
    contry_id = Column("contry_id", Integer(), primary_key=True) # id del pais 
    contry_name = Column("contry_name", String(50), unique=True) # nombre del pais



class Store(Base):
    __tablename__= "stores"
    __column__ = ["store_id", "contry_id_fk", "store_name", "link_store"]
    __column_db__ = ["store_id", "contry_id", "store_name", "link_store"]
    
    def __str_create__(data, error=True):
        if error:
            print(f"Creando la tienda '{data['store_name']}'.")
        else:
            print(f"Error, la tienda '{data['store_name']}' ya existe y no pueden existir dos store_name iguales.")
    
    store_id = Column("store_id", Integer(), primary_key=True) # id de la tienda
    contry_id_fk = Column("contry_id_fk", Integer(), ForeignKey("contries.contry_id")) # id del id del pais al que pertenece
    store_name = Column("store_name", String(100), unique=True) # nombre de la tienda
    link_store = Column("link_store", Text()) # link de la tienda



# en construccion
# class Match_product(Base):
#     __tablename__ = "match_products"

#     match_id = Column("match_id", Integer(), primary_key=True)
    



class User(Base):
    __tablename__ = "users"
    __column__ = ["user_id", "rol_id_fk", "user_name", "first_name", "last_name"]
    __column_db__ = ["user_id", "rol_id", "user_name", "first_name", "last_name"]
    
    def __str_create__(data, error=True):
        if error:
            print(f"Creando el usuario '{data['user_name']}'.")
        else:
            print(f"Error, el usuario '{data['user_name']}' ya existe y no pueden existir dos user_name iguales.")
    
    user_id = Column("user_id", Integer(), primary_key=True)
    rol_id_fk = Column("rol_id_fk", Integer(), ForeignKey("roles.rol_id"))
    user_name = Column("user_name", String(100), unique=True)
    first_name = Column("first_name", String(100))
    last_name = Column("last_name", String(100))
    #ip = Column("ip", String())



class Rol(Base):
    __tablename__ = "roles"
    __column__ =  ["rol_id", "rol_type"]
    __column_db__ = __column__
    
    def __str_create__(data, error=True):
        if error:
            print(f"Creando el rol '{data['rol_type']}'.")
        else:
            print(f"Error, el Rol '{data['rol_type']}' ya existe y no pueden existir dos rol_type iguales.")
    
    rol_id = Column("rol_id", Integer(), primary_key=True)
    rol_type = Column("rol_type", String(100), unique=True)