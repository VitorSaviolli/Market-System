from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database.dbase import SessionLocal
from database import crud
from api.schemas import SaleCreate, SaleResponse

router = APIRouter(
    prefix="/sales", #Todas as rotas começam com /sales
    tags=["Vendas"] #visivel em /docs
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#C -> CREATE
#criar venda
@router.post("/", response_model=SaleResponse, status_code=201)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    #Converte lista de Pydantic models para dicts
    #[SaleItemCreate, SaleItemCreate] -> [dict, dict]
    products_data = [item.model_dump() for item in sale.products]

    new_sale = crud.create_sale(db, products_data, sale.payment_method)

    if not new_sale:
        raise HTTPException(
            status_code=400,
            detail="Erro ao criar venda. Verificar estoque e produto"
        )
    return new_sale


#Listar as vendas
#R -> RECEIVE
@router.get("/",response_model=List[SaleResponse])
def get_all_sales(db: Session = Depends(get_db)):
    sales = crud.get_all_sales(db)
    return sales

