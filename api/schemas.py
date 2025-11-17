from pydantic import BaseModel, Field
from typing import Optional,List
from datetime import datetime

# ProductBase herda de BaseModel
# Isso torna ProductBase um schema Pydantic
# Ganha automaticamente:
# Validação de tipos
# Conversão automática de dados
# Mensagens de erro detalhadas
# Serialização JSON
class ProductBase(BaseModel): #torna um schema Pydantic
    #"atributo": tipo = Field(...,.,.,descricao="..") gt = greater, ge = greater or equal
    # ... = Field(...) -> ... = Campo obrigatorio(Elipsis)
    name: str = Field(...,min_length=1,max_length=200,description="Nome do Produto")
    price: float = Field(...,gt=0,description="Preço deve ser maior que 0")
    stock: int = Field(...,ge=0, description="Estoque deve ser maior ou igual a 0")
    description: Optional[str] = Field(None, max_length=500, description="Descrição")

class ProductCreate(ProductBase):
    # herda TUDO de schemas.py sem adicionar nada novo
    #name: str = Field(..., min_length=1, max_length=200, description="Nome do Produto")
    #price: float = Field(..., gt=0, description="Preço deve ser maior que 0")
    #stock: int = Field(..., ge=0, description="Estoque deve ser maior ou igual a 0")
    #description: Optional[str] = Field(None, max_length=500, description="Descrição")"
    pass # Evita repetir código

class ProductUpdate(BaseModel): #Nao herda ProductBase para nao obrigar a trocar todos os campos
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None,ge=0)
    description: Optional[str] = Field(None, max_length=500)

class ProductResponse(ProductBase): #herda de product base para pegar os campos
    #Usado quando a API retorna dados de produtos(GET,POST,PUT)
    id:int #isso para ProductBase possuir um ID | adiciona o campo id
    #Nao foi feito o ID direto no ProductBase para evitar conflito com o Pydantic
    class Config:
        from_attributes = True #permite converter do SQLACLCHEMY (ORM)
        
class SaleItemCreate(BaseModel):
    product_id: int = Field(...,gt=0,description="ID do produto")
    quantity: int = Field(...,gt=0,description="Quantidade do produto")

class SaleCreate(BaseModel):
    """
    {
        "products": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ],
        "payment_method": "Dinheiro"
    }
    """
     
    products: List[SaleItemCreate] = Field(...,min_length=1, description="Lista de Produtos")
    payment_method: str = Field(...,min_length=1,description="Metodo de Pagamento")

class SaleResponse(BaseModel):
    id: int
    date: datetime
    total: float
    payment_method: str

    class Config:
        from_attributes = True
    
