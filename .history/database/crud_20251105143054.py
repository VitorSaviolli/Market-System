from sqlalchemy.orm import Session
from database.models import Product, Sale
from typing import List, Optional
#Optional -> pode retorna nulo ou string/int/float etc

def create_product(session: Session, name: str, price: float, stock: int, description: str = None):
    new_product= Product(
        name=name,
        price=price,
        stock=stock,
        description=description
    )
    #add
    session.add(new_product)
    #commit
    session.commit()
    #Atualiza o objeto com dados do banco
    session.refresh(new_product)
    return new_product

def get_all_products(session: Session) -> List[Product]:
    return session.query(Product).all()

def get_product_by_id(session: Session, product_id:int) -> Optional[produ]:
    return session.query(Product).filter(Product.id == product_id).first()

def update_product(session:Session, product_id: int, **kwargs):
    product = get_product_by_id(session,product_id)

    if product:
        for key, value in kwargs.items():
            #hasattr(objeto, 'nome_do_atributo')
            #se o atributo existe -> ? true:false
            if hasattr(product,key):

                setattr(product, key, value)