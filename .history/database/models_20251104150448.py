from sqlalchemy import Column, Integer,String, Float, DataTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

#tabela para produtos que estão em venda
sales_products = Table(
    'sale_products',
    Base.metadata,
    Column('sale_id', Integer, ForeignKey('sales.id')),
    Column('product_id', Integer, ForeignKey("products.id")),
    Column('quantity', Integer, nullable=False),
    Column('unit_price', Float, nullable=False)
)
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100),nullable=False)
    price = Column(Float,nullable=False)
    stock = Column(Integer, default=0)
