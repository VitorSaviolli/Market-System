from sqlalchemy import Column,Inteer,String, Float, DataTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

sales_products = Table(
    'sale_products',
    Base.metadata
)
