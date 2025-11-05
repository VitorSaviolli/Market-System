from sqlalchemy import Column, Integer,String, Float, DataTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import DateTime
from database.database import Base

#tabela para produtos que estão em venda
sales_products = Table(
    'sale_products',
    Base.metadata,
    Column('sale_id', Integer, ForeignKey('sales.id')),
    Column('product_id', Integer, ForeignKey("product.id")),
    Column('quantity', Integer, nullable=False),
    Column('unit_price', Float, nullable=False)
)
class Product(Base):
    pass