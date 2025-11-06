# 🛒 Market System

Sistema de gerenciamento de mercado desenvolvido em Python com SQLAlchemy e Tkinter.

**Lembrando que o sistema está sendo feito inteiro "à mão" sem "copia e cola", isso para focar no aprendizado de banco de dados e APIs.**

## 📋 Sobre o Projeto

Sistema completo para gerenciar produtos e vendas de um mercado, incluindo:
- Cadastro de produtos
- Controle de estoque
- Registro de vendas
- Relacionamento entre produtos e vendas
- Operações CRUD completas
- Validação de estoque em tempo real

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados relacional
- **Tkinter** - Interface gráfica (em desenvolvimento)

## 📁 Estrutura do Projeto

```
market_system/
│
├── database/
│   ├── __init__.py
│   ├── dbase.py          # Configuração do banco de dados e engine
│   ├── models.py         # Modelos (Product, Sale, sales_products)
│   └── crud.py           # Operações CRUD completas
│
├── test_crud.py          # Testes das funcionalidades
├── venv/                 # Ambiente virtual (não versionado)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🗄️ Modelos de Dados

### Product (Produtos)
- `id` - Identificador único (auto-incremento)
- `name` - Nome do produto (obrigatório)
- `price` - Preço (obrigatório)
- `stock` - Quantidade em estoque (padrão: 0)
- `description` - Descrição (opcional)

### Sale (Vendas)
- `id` - Identificador único (auto-incremento)
- `date` - Data da venda (gerada automaticamente com `datetime.now`)
- `total` - Valor total (obrigatório)
- `payment_method` - Forma de pagamento (obrigatório)

### sales_products (Tabela Intermediária)
- `sale_id` - ID da venda (FK → sales.id)
- `product_id` - ID do produto (FK → products.id)
- `quantity` - Quantidade vendida (obrigatório)
- `unit_price` - Preço unitário no momento da venda (obrigatório)

### Relacionamento
- **Muitos-para-Muitos** entre produtos e vendas através da tabela intermediária `sales_products`

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SEU-USUARIO/market_system.git
cd market_system
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🔧 Funcionalidades Implementadas

### ✅ CRUD de Produtos

- `create_product()` - Criar produto
- `get_all_products()` - Listar todos os produtos
- `get_product_by_id()` - Buscar produto por ID
- `update_product()` - Atualizar produto (com **kwargs)
- `delete_product()` - Deletar produto

### ✅ CRUD de Vendas

- `create_sale()` - Criar venda com múltiplos produtos
  - Calcula total automaticamente
  - Diminui estoque automaticamente
  - Insere dados na tabela intermediária
- `get_all_sales()` - Listar todas as vendas
- `get_sale_by_id()` - Buscar venda por ID

## 🧪 Como Testar

Execute o arquivo de testes:

```bash
python test_crud.py
```

O teste irá:
1. Criar 5 produtos (Arroz, Feijão, Açúcar, Café, Óleo)
2. Listar todos os produtos
3. Buscar produto por ID
4. Atualizar um produto
5. Criar uma venda com múltiplos produtos
6. Listar todas as vendas

## 📝 Em Desenvolvimento

- [ ] Interface gráfica com Tkinter
- [ ] Tela de cadastro de produtos
- [ ] Tela de registro de vendas
- [ ] Relatórios de vendas
- [ ] Sistema de autenticação
- [ ] Validações adicionais

## 💡 Conceitos Aprendidos

- ORM (Object-Relational Mapping) com SQLAlchemy
- Relacionamentos muitos-para-muitos
- Operações CRUD
- Type hints em Python
- Gerenciamento de sessões de banco de dados
- Transações e commits

## 📄 Licença

Este projeto está sob a licença MIT - sinta-se livre para usar como aprendizado.
```