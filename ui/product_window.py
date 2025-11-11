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