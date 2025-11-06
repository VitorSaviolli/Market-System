from database.dbase import SessionLocal, engine, Base
from database.crud import *
from database.models import Product, Sale

#cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

session = SessionLocal()

print("=== TESTE 1: CRIAR PRODUTOS ===")
#estrutura para se quiser cadastrar algum produto
#{"name": nome_produto, "price": preço_do_produto, "stock": quantidade_stock, "description": "descrição_do_produto"}
produtos_cadastrar = [
    {"name": "Arroz", "price": 10.50, "stock": 100, "description": "Arroz branco"},
    {"name": "Feijão", "price": 8.00, "stock": 50, "description": "Feijão Preto"},
    {"name": "Açúcar", "price": 5.00, "stock": 80, "description": "Açúcar refinado"},
    {"name": "Café", "price": 15.00, "stock": 30, "description": "Café preto"},
    {"name": "Óleo", "price": 7.00, "stock": 40, "description": "Óleo de cozinha"}
]

produtos_criados = []
for item in produtos_cadastrar:
    produto = create_product(
        session,
        name=item["name"],
        price=item["price"],
        stock=item["stock"],
        description=item["description"]
    )
    produtos_criados.append(produto)
    print(f" Produto criado: {produto.name} - R${produto.price}")

print(f"Total de produtos cadastrados: {len(produtos_criados)}")

print("TESTE 2: LISTAR PRODUTOS")
produtos = get_all_products(session)
for p in produtos:
    print(f"ID: {p.id} | NOME: {p.name} | PREÇO: R${p.price} | ESTOQUE: {p.stock} | DESCRIÇÃO: {p.description}")

print("TESTE 3: BUSCAR PRODUTO POR ID")
produto = get_product_by_id(session, 1)
print(f"Produto encontrado: {produto.name} - R${produto.price}")

print("TESTE 4: ATUALIZAR PRODUTO")
update_product(session, 1, price=12.00, stock=120)
produto_atualizado = get_product_by_id(session, 1)
print(f"Produto atualizado: {produto_atualizado.name} | Preço: R${produto_atualizado.price} | Estoque: {produto_atualizado.stock}")

print("TESTE 5: CRIAR VENDA")
produtos_venda = [
    {'product_id': 1, 'quantity': 2},
    {'product_id': 2, 'quantity': 1}
]
venda = create_sale(session, produtos_venda, "Dinheiro")
if venda:
    print(f"Venda criada: ID: {venda.id} | Total: R${venda.total} | Data: {venda.date}")
else:
    print("Erro ao criar venda!")

print("TESTE 6: LISTAR VENDAS")
vendas = get_all_sales(session)
for v in vendas:
    print(f"ID: {v.id} | Total: R${v.total} | Data: {v.date} | Forma de Pagamento: {v.payment_method}")

#fechar sessão
session.close()
print("TESTES CONCLUÍDOS!")