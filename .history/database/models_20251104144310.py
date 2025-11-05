from sqlalchemy import Column,Inteer,String, Float, DataTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

#tabela para produtos que estão em venda
sales_products = Table(
    'sale_products',
    Base.metadata
)
