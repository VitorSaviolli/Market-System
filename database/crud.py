from sqlalchemy.orm import Session
from database.models import Product, Sale, sales_products
from typing import List, Optional
#Optional -> pode retorna nulo ou string/int/float etc
#função para criar produtos                      
# #Função para validar produto antes de criar/ataulizar
def validate_product_data(name: str = None, price: float = None, stock: int = None):
    if name is not None and len(name.strip()) == 0:
        raise ValueError("Nome do produto não pode ser vazio")
    
    if price is not None and price < 0:
        raise ValueError("Preço não pode ser negativo -> price >= 0")
    
    if stock is not None and stock < 0:
        raise ValueError("Estoque não pode ser negativo -> stock >= 0")
                             #desc: opcional
def create_product(session: Session, name: str, price: float, stock: int, description: str = None):
    #valida os dados antes de criar
    validate_product_data(name=name, price=price, stock=stock)

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
        validate_product_data(
            name=kwargs.get('name'),
            price=kwargs.get('price'),
            stock=kwargs.get('stock')
        )
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

#Função para remover duplicados
#keep: Parâmetro que decide qual produto MANTER baseado no ID, (primeiro ID ou ultimo ID?)
def remove_duplicate_products(session:Session, keep: str = "first") -> int:
    from sqlalchemy import func
    #func: permite usar funções SQL como:
    # COUNT(), SUM(), AVG(), MAX(), MIN()

    duplicates = (
        session.query(Product.name, func.count(Product.id)) #quantas vezes esse nome aparece
        .group_by(Product.name)
        #Antes:
        # ID | Nome
        # ---|-----
        # 1  | Café
        # 2  | Café
        # 3  | Arroz
        # 4  | Café
        # Depois do GROUP BY:
        # Grupo "Café": [1, 2, 4]  → Count = 3
        # Grupo "Arroz": [3]       → Count = 1
        .having(func.count(Product.id) > 1) #se for maior que um quer dizer que é duplicado
        .all() #executa a query e retorna todos os resultados
    )

    merged_count = 0
    
    for name, count in duplicates:
        products = (
            session.query(Product)
            .filter(Product.name == name)
            .order_by(Product.id)
            .all()
        )
        if keep == "first": #mantem o primeiro ID do produto e junta para deletar o resto
            main_product = products[0] # mantem o produto 0
            to_merge = products[1:] # para deletar depois pega depois do produto 0
        #keep == "last" (qualquer coisa vai entender como último)
        else:
            main_product = products[-1]
            to_merge = products[:-1]

        #======JUNTA TODOS OS ESTOQUES DOS ITENS DUPLICADOS====
        total_stock = main_product.stock
        for product in to_merge:
            total_stock += product.stock

        main_product.stock = total_stock
        #======================================================

        #deleta os duplicados
        for product in to_merge:
            session.delete(product)
            merged_count += 1
            print(f" Mesclado: {product.name} (ID:{product.id})")
        print (f"Produto final: {main_product.name} (ID: {main_product.id})")
    session.commit()
    return merged_count

#Função para criar uma venda com produtos
def create_sale(session:Session, products: List[dict], payment_method: str):
    """
    products = [
        {'product_id': 1, 'quantity': 2},
        {'product_id': 2, 'quantity': 1} #exemplos
    ]
    """
    total = 0
    sale_items = []

    for item in products:
        product = get_product_by_id(session, item['product_id'])
        # O produto existe?
        if not product:
            raise ValueError (f"Produto com ID {item['product_id']} não encontrado")
        # Quantidade Valida?
        if item['quantity'] <= 0:
            raise ValueError(f"Quantidade deve ser maior que zero. Produto: {product.name}")
        # Tem estoque o suficiente ?
        if product.stock < item['quantity']:
            raise ValueError(
                f"Estoque insuficiente para {product.name}"
                f"Disponível: {product.stock}, Solicitado: {item['quantity']}"
            )
        
        subtotal = product.price * item['quantity']
        total += subtotal

        #subtrair do stock
        product.stock -= item['quantity']

        sale_items.append({
            'product': product,
            'quantity': item['quantity'],
            'unit_price': product.price
        })

    new_sale = Sale(
        total=total,
        payment_method=payment_method
    )
        
    session.add(new_sale)
    session.flush() # Gera o id da venda sem fazer commit

    #for para inserir prdutos na tabela de relacionamentos
    for item in sale_items:
        # STATMENT para comandos SQL, nesse caso INSERT 
        stmt = sales_products.insert().values(
            sale_id=new_sale.id,
            product_id=item['product'].id,
            quantity=item['quantity'],
            unit_price=item['unit_price']
        )
        session.execute(stmt)

    session.commit()
    session.refresh(new_sale)

    return new_sale
        
#Função para buscar detalhes de uma venda (produtos vendidos)
def get_sale_details(session:Session, sale_id: int ) -> dict:
    sale = get_sale_by_id(session, sale_id)
    if not sale:
        return None #Venda não existe

    from sqlalchemy import select
    stmt = select(
        sales_products.c.product_id, # SELECT product_id FROM sales_products;
        sales_products.c.quantity,
        sales_products.c.unit_price
    ).where(sales_products.c.sale_id == sale_id)

    items = session.execute(stmt).fetchall()

    products_list = []
    for item in items:
        product = get_product_by_id(session, item.product_id)
        if product:
            products_list.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
                'subtotal': float(item.quantity * item.unit_price)
            })
        
    return {
        'sale_id': sale.id,
        'date': sale.date,
        'total': float(sale.total),
        'payment_method': sale.payment_method,
        'products': products_list
    }

#Função para cancelar venda (deletar e devolver o estoque)(cancelar stmt)
def cancel_sale(session: Session, sale_id: int) -> bool:
    sale = get_sale_by_id(session, sale_id)
    if not sale:
        return False
    
    from sqlalchemy import select, delete
    
    stmt = select(
        sales_products.c.product_id,
        sales_products.c.quantity
    ).where(sales_products.c.sale_id == sale_id)

    items = session.execute(stmt).fetchall()

    for item in items:
        product = get_product_by_id(session, item.product_id)
        if product:
            product.stock += item.quantity

    delete_stmt = delete(sales_products).where(sales_products.c.sale_id == sale_id)
    session.execute(delete_stmt)

    session.delete(sale)
    session.commit()
    print(f"Venda #{sale_id} cancelada com sucesso")
    return True

    
    
    
    # for item in products:
    #     product = get_product_by_id(session, item['product_id'])
    #     if product and product.stock >= item['quantity']:
    #             #Calcular o subtotal
    #             subtotal = product.price * item['quantity']
    #             total += subtotal
    #             #diminui do estoque
    #             product.stock -= item['quantity']
    #             #adiciona o produto à venda
    #             sale_items.append({
    #                 'product': product,
    #                 'quantity': item['quantity'],
    #                 'unit_price': product.price
    #             })
    #     else:
    #         return None #não existe ou sem estoque
        
    # #Criar venda
    # new_sale = Sale(
    #     total=total,
    #     payment_method = payment_method
    # )

    # session.add(new_sale)
    # session.flush()

    # for item in sale_items:
    #     # STATMENTE para comando INSERT SQL
    #     stmt = sales_products.insert().values(
    #         sale_id=new_sale.id,
    #         product_id=item['product'].id,
    #         quantity=item['quantity'],
    #         unit_price=item['unit_price']
    #     )
    #     session.execute(stmt)
    # #salva quaisquer alterações
    # session.commit()
    # session.refresh(new_sale)

    # return new_sale

#Função que retorna todas as vendas
def get_all_sales(session:Session) -> List[Sale]:
    return session.query(Sale).all()

def get_sale_by_id(session:Session, sale_id: int) -> Optional[Sale]:
    return session.query(Sale).filter(Sale.id == sale_id).first()
