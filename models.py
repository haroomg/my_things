from sqlalchemy import Column, Integer, Float, Boolean, String, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()



class Product(Base):
    __tablename__ = "products"
    __column__ = [
        "product_id", "store_id", "product_type_id", "currency_id", "link", "title", "description", "product_brand", "img_urls", "img_direction_folder", "price", "discount_price", "has_discount", "characteristics"
        ]
    __foreignKey__ = ["store_id", "product_type_id", "currency_id",]
    __unique__ = "link"
    
    def __str__(data: dict = None, msm: str = "create" ) -> str:
        
        if msm == "create":
            print(f"PRODUCT - Se acaba de crear uno o varios productos.")
        elif msm == "update":
            print(f"PRODUCT - Se acaba de actualizar uno o varios productos")
        elif msm == "delete":
            print(f"PRODUCT - Se acaba de eliminar uno o varios productos")
        elif msm == "erro":
            print(f"PRODUCT - Error a la hora de crear uno o varios productos, puede ser que el link del producto se este repietiendo o que el el Product_id ya existe")
    
    
    product_id = Column("product_id", Integer, primary_key=True, unique=True) # id del producto
    store_id = Column("store_id", Integer(), ForeignKey("stores.store_id")) # id de la tienda y su link
    product_type_id = Column("product_type_id", String(256), ForeignKey("type_products.product_type_id")) # id del tipo de producto al que corresponde
    currency_id = Column("currency_id", ForeignKey("currencies.currency_id"))
    
    link = Column("link", Text(), unique=True) # link del producto
    title = Column("title", Text()) # titulo del producto, con este es que se va a realizar la busqueda
    description = Column("description", Text()) #descripcion del producto
    product_brand = Column("product_brand", String(256)) # nombre de la marca del producto 
    
    img_urls = Column("img_urls", Text()) # urls de las imagenes del producto
    img_direction_folder = Column("img_direction_folder", Text()) # Nombre y direncion en carpeta donde se encuentra la imagen descargada
    
    price = Column("price", Float()) # precio
    discount_price = Column("discount_price", Float()) # precio del producto con descuento
    has_discount = Column("has_discount", Boolean()) # valor buleano para decir si tiene un producto
    characteristics = Column("characteristics", JSON()) # json con las carcateristicas del producto



class Type_product(Base):
    __tablename__ = "type_products"
    __column__ = ["product_type_id", "product_type_name"]
    __foreignKey__ = False
    __unique__ = "product_type_name"
    
    
    def __str__(data: dict = None, msm: str = "create" ) -> str:
        
        if msm == "create":
            print(f"TYPE_PRODUCT - Se acaba de crear uno o varios tipos de producto.")
        elif msm == "update":
            print(f"TYPE_PRODUCT - Se acaba de actualizar uno o varios tipos de producto")
        elif msm == "delete":
            print(f"TYPE_PRODUCT - Se acaba de eliminaruno o varios tipos de producto")
        elif msm == "erro":
            print(f"TYPE_PRODUCT - Error a la hora de crear uno o varios tipos de producto, puede ser que el tipo de producto se este repietiendo o que el el product_type_id ya existe")
    
    
    product_type_id = Column("product_type_id", Integer(), primary_key=True, unique=True) # id tipo de producto
    product_type_name = Column("product_type_name", String(50), unique=True) # nombre del tipo de producto



class Currency(Base):
    __tablename__ = "currencies"
    __column__ = ["currency_id", "currency_name", "symbol"]
    __foreignKey__ = False
    __unique__ = "currency_name"
    
    
    def __str__(data: dict = None, msm: str = "create" ) -> str:
        
        if msm == "create":
            print(f"CURRENCY - Se acaba de crear una o varias divizas.")
        elif msm == "update":
            print(f"CURRENCY - Se acaba de actualizar una o varias divizas")
        elif msm == "delete":
            print(f"CURRENCY - Se acaba de eliminar una o varias divizas")
        elif msm == "erro":
            print(f"CURRENCY - Error a la hora de crear una o varias divizas, puede ser que el tipo de diviza se este repietiendo o que el el currency_id ya existe")
            
            
    
    currency_id = Column("currency_id", Integer(), primary_key=True, unique=True) # id de la diviza
    currency_name = Column("currency_name", String(50), unique=True) # nombre de la diviza
    symbol = Column("symbol", String(20))



class Contry(Base):
    __tablename__ = "contries"
    __column__ = ["contry_id", "contry_name"]
    __foreignKey__ = False
    __unique__ = "contry_name"
    
    
    def __str__(data: dict = None, msm: str = "create" ) -> str:
        
        if msm == "create":
            print(f"CONTRY - Se acaba de crear uno o varios paises.")
        elif msm == "update":
            print(f"CONTRY - Se acaba de actualizar uno o varios paises")
        elif msm == "delete":
            print(f"CONTRY - Se acaba de eliminar uno o varios paises")
        elif msm == "erro":
            print(f"CONTRY - Error a la hora de crear uno o varios paises, puede ser que el pais se este repietiendo o que el el contry_id ya existe")
            
    
    contry_id = Column("contry_id", Integer(), primary_key=True, unique=True) # id del pais 
    contry_name = Column("contry_name", String(50), unique=True) # nombre del pais



class Store(Base):
    __tablename__= "stores"
    __column__ = ['store_id', "contry_id", "store_name", "link_store"]
    __foreignKey__ = ["contry_id"]
    __unique__ = "store_name"
    
    
    def __str__(data: dict = None, msm: str = "create" ) -> str:
        
        if msm == "create":
            print(f"STORE - Se acaba de crear una o varias tiendas.")
        elif msm == "update":
            print(f"STORE - Se acaba de actualizar una o varias tiendas")
        elif msm == "delete":
            print(f"STORE - Se acaba de eliminaruna o varias tiendas")
        elif msm == "erro":
            print(f"STORE - Error a la hora de crear una o varias tiendas, puede ser que la tienda se este repietiendo o que el el store_id ya existe")
    
    store_id = Column("store_id", Integer(), primary_key=True, unique=True) # id de la tienda
    contry_id = Column("contry_id", Integer(), ForeignKey("contries.contry_id")) # id del id del pais al que pertenece
    store_name = Column("store_name", String(100),  unique=True) # nombre de la tienda
    link_store = Column("link_store", Text(), unique=True) # link de la tienda




class Match_product(Base): # esta inconcluso
    __tablename__ = "match_products"

    match_id = Column("match_id", Integer(), primary_key=True, unique=True)
    __column__ = []
    __foreignKey__ = False



class User(Base):
    __tablename__ = "users"
    __column__ = ["user_id", "rol_id", "user_name", "first_name"]
    __foreignKey__ = ["rol_id"]
    __unique__ = "user_name"
    
    
    def __str__(data: dict = None, msm: str = "create" ) -> str:
        
        if msm == "create":
            print(f"USER - Se acaba de crear uno o varios usuario.")
        elif msm == "update":
            print(f"USER - Se acaba de actualizar uno o varios usuarios")
        elif msm == "delete":
            print(f"USER - Se acaba de eliminar uno o varios usuarios")
        elif msm == "erro":
            print(f"USER - Error a la hora de crear uno o varios usuarios, puede ser que el usuario se este repietiendo o que el el user_id ya existe")
            
            
    
    user_id = Column("user_id", Integer(), primary_key=True, unique=True)
    rol_id = Column("rol_id", Integer(), ForeignKey("roles.rol_id"))
    user_name = Column("user_name", String(100), unique=True)
    first_name = Column("first_name", String(100))
    last_name = Column("last_name", String(100))



class Rol(Base):
    __tablename__ = "roles"
    __column__ = ["rol_id","rol_type"]
    __foreignKey__ = False
    __unique__ = "rol_type"
    
    def __str__(data: dict = None, msm: str = "create" ) -> str:
        
        if msm == "create":
            print(f"USER - Se acaba de crear un o varios roles")
        elif msm == "update":
            print(f"USER - Se acaba de actualizar uno o varios roles")
        elif msm == "delete":
            print(f"USER - Se acaba de eliminar uno o varios roles")
        elif msm == "erro":
            print(f"USER - Error a la hora de crear un nuevo rol, puede ser que el rol se este repietiendo o que el el rol_id ya existe")
    
    rol_id = Column("rol_id", Integer(), primary_key=True, unique=True)
    rol_type = Column("rol_type", String(100), unique=True)