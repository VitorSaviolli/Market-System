from sqlalchemy import Session
from database.models import Product, Sale
from typing import List, Optional

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

def get_product_by_id(session: Session, product_id)

def update_product(session:Session, product_id: int, **kwargs):
    product = get_product_by_id(session,product_id)