from sqlalchemy import Session
from database.models import Product, Sale
from typing import List, Optional

def create_product(session: Session, name: str, price)