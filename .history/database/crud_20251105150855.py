from sqlalchemy.orm import Session
from database.models import Product, Sale
from typing import List, Optional
#Optional -> pode retorna nulo ou string/int/float etc
#função para criar produtos
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

#função para retornar todos os produtos
def get_all_products(session: Session) -> List[Product]:
    return session.query(Product).all()

#função para procurar por id
def get_product_by_id(session: Session, product_id:int) -> Optional[Product]:
    return session.query(Product).filter(Product.id == product_id).first()
#função para atualizar produtos
def update_product(session:Session, product_id: int, **kwargs):
    product = get_product_by_id(session,product_id)

    if product:
        for key, value in kwargs.items():
            #hasattr(objeto, 'nome_do_atributo')
            #se o atributo existe -> ? true:false
            if hasattr(product,key):
                #dentro de Product -> key ter o valor de value
                setattr(product, key, value)
        #salva quaisquer alterações
        session.commit()
        session.refresh(product)
        return product
    
    return None

#Função para deletar produtos
def delete_product(session: Session, product_id: int):
    product = get_product_by_id(session, product_id)

    if product:
        session.delete(product)
        session.commit()
        return True
    
    return False

#Função para criar uma venda com produtos
def create_sale(session:Session, products: List[dict], payment_method: str):
    """
    products = [
        {'product_id': 1, 'quantity': 2},
        {'product_id': 2, 'quantity': 1} #exemplos
    ]
    """
    total = 0
    sale_products = []

    for item in products:
        product = get_product_by_id(session, item['product_id'])
        if product and product.stock >= item['quantity']:
                #Calcular o subtotal
                subtotal = product.price * item['quantity']
                total += subtotal
                #diminui do estoque
                product.stock -= item['quantity']
                #adiciona o produto à venda
                sale_products.append(product)
        else:
            return None #não existe ou sem estoque
        
    #Criar venda
    new_sale = Sale(
        total=total,
        payment_method = payment_method
    )

    new_sale.products = sale_products

    #salva quaisquer alterações
    session.add(new_sale)
    session.commit()
    session.refresh(new_sale)

    return new_sale

def get_all_sales(session:Session) -> List[Sale]:
