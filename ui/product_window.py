import tkinter as tk
from tkinter import ttk, messagebox
from database.dbase import SessionLocal
from database.crud import create_product, get_all_products, update_product, delete_product
from database.models import Product

class ProductWindow:
    def __init(self,root, mode="register"):
        #Cria uma janela secundaria
        self.window = tk.Toplevel(root)
        self.window.title("Gerenciamento de Produtos")
        self.window.geometry("900x600")
        self.center_window()
        self.session = SessionLocal()
        self.mode = mode

        self.select_product_id = None

        self.create_widgets()
        
        if mode == "list":
            self.load_products()

    def center_window(window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    #func para criar elementos principais na tela
    def create_widges(self):
        main_frame = ttk.Frame(self.window, padding="20")  #Espaçamento de 20px
        main_frame.grid(row=0,column=0,stick=(tk.W,tk.E,tk.N,tk.S))

        title = ttk.Label(
            main_frame,
            text="Cadastro de Produto",
            font=("Arial", 18, "bold")
        )
        
        title.grid(row=0,column=0, columnspan=2, pady=20) #ocupa duas colunas
        #form de cadastro
        form_frame = ttk.LabelFrame(main_frame,text="Dados do Produto",padding=10)
        form_frame.grid(row=1, column=0, columnspan=2, stick=(tk.W,tk.E),pady=10)
        
        #campo:nome
        ttk.Label(form_frame, text="Nome").grid(row=0,column=0,stick=(tk.W),pady=5)
        self.name_entry = ttk.Entry(form_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        #campo:estoque
        ttk.Label(form_frame,text="Estoque:").grid(row=0,column=0,sticky=(tk.W, tk.E, tk.N, tk.S))