from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import products,sales
from database.dbase import engine, Base

#Cria as tabelas no banco (caso elas não existam)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title= "Market System Api",
    description="API REST para gerenciamento de mercado - Produtos e Vendas",
    version="1.0.0",
    docs_url="/docs", #Swagger UI
    redoc_url="/redoc" # ReDoc (documentação alternativa)
)

#Configura CORS(Cross-Origin Resource Sharing)
#Necessário para o front acessar a API
#tradução: Use o middleware de CORS para controlar quem pode acessar minha API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Sites, app, qualquer lugar pode fazer requisições
    allow_credentials=True, # Permite envio de cookies
    allow_methods=["*"], #Permite todos os métodos de API (GET,POST,PUT,PATCH,DELETE,OPTIONS...)
    allow_headers=["*"] #Permite todos os headers
)
#Rotas de produto (/products)
app.include_router(products.router)

#Rotas de vendas (/sales)
app.include_router(sales.router)

#Rota raiz (/)
#Retorna informações básicas e link para documentação da API
@app.get("/")
def read_root():
    return{
        "message": "Market System API",
        "version": "1.0.0",
        "docs": "/docs",
        "routes":{
            "products":"/products",
            "sales":"/sales"
        }
    }

#Rota para verificar se a API está online(health_check)
@app.get("/health")
def health_check():
    return{
        "status": "healthy",
        "message": "API está funcionando"
    }

