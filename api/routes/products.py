from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database.dbase import SessionLocal
from database import crud
from api.schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(
    prefix="/products", #todas as rotas começaram com /products
    tags=["Produtos"] #visivel em /docs
)

def get_db():
    db = SessionLocal() # db é um tipo Session
    try:
        yield db #retorna a sessão e mantém ela aberta
    finally:
        db.close() #Fecha a sessão mesmo se der erro

#============FAZENDO CRUD===================================================
@router.post("/", response_model=ProductResponse, status_code=201)
#Depends: Antes de chamar POST / o depends ele:
# chama a função get_db() -> pega o valor retornado (no caso o que vem do yield)
# -> passa esse valor para o parâmetro db da função create_product
#C -> CREATE
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
        Cria um novo produto
        - name: Nome do produto
        - price: Preço do produto
        - stock: Estoque do produto
        - description: Descrição do produto(opcional)
        obs: retorna o ID por causa do ProductCreate
        retorna: O produto criado com ID gerado pela banco
    """
    new_product = crud.create_product(
        db, #Session
        name=product.name,
        price=product.price,
        stock=product.stock,
        description=product.description
    )
    return new_product

#retorna todos os produtos na query
#R -> RECEIVE
@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = crud.get_all_products(db) #lista todos os produtos 
    return products

#mescla produtos e exclui duplicados
@router.post("/merge-duplicates", status_code=200)
def merge_duplicates(keep: str = "first", db: Session = Depends(get_db)):
    if keep not in ["first", "last"]:
        raise HTTPException(
            status_code=400,
            detail="Parâmetro 'keep' deve ser 'first' ou 'last' "
        )
    
    merged_count = crud.remove_duplicate_products(db,keep=keep)
    if merged_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Nenhum produto duplicado encontrado"
        )
    return {
        "message": f"{merged_count} produtos duplicados foram mesclados",
        "merged_count": merged_count,
        "kept": keep
    }

#procure por ID um produto
#R -> RECEIVE
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session= Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail = "Produto não encontrado")
    return product

#Atualiza um produto existente
#U -> UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    #Converte para dict e remove valores None
    update_data = product.model_dump(exclude_unset=True)

    updated_product = crud.update_product(db, product_id, **update_data)#**kwargs
    
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated_product


#deletar produto
#D -> DELETE
@router.delete("/{product_id}",status_code=204)   
def delete_product(product_id: int, db: Session = Depends(get_db)):                
    success = crud.delete_product(db, product_id)

    if not success:
        raise HTTPException(status_code=404, detail = "Produto não encontrado")
    return None # 204 sem conteudo

#deletar varios produtos
#D -> DELETE
@router.delete("/", status_code=204)
def delete_multiple_products(products_ids: List[int], db:Session = Depends(get_db)):
    deleted_count = 0
    not_found = []

    for product_id in products_ids:
        success = crud.delete_product(db, product_id)
        if success:
            deleted_count += 1
        else:
            not_found.append(product_id)
    if not_found:
        raise HTTPException(
            status_code=404,
            detail=f"Produto não encontrado: {not_found}"
        )
    return None #Sem conteudo

#deleta produtos por intervalo
#D -> DELETE
@router.delete("/range",status_code=204)
def delete_products_range(
    start_id: int, 
    end_id: int,
    confirm: bool = True, # Ter confirmação da ação de delete 
    db: Session = Depends(get_db)
    ):
    if start_id > end_id:
        raise HTTPException(
            status_code=400,
            detail=f"start_id ({start_id}) deve ser menor que ou igual ao end_id({end_id})"
        )
    if start_id < 1:
        raise HTTPException(
            status_code=400,
            detail="start_id deve ser maior que 0"
        )
    deleted_count =0
    not_found = []
    for product_id in range(start_id, end_id + 1):
        success = crud.delete_product(db, product_id)
        if success:
            deleted_count += 1
        else:
            not_found.append(product_id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum produto encontrado no intervalo de {start_id} até {end_id}"
        )
    return None #204 sem conteudo