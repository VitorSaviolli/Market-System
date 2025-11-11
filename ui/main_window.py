import tkinter as tk
from tkinter import ttk
from ui.product_window import ProductWindow
from ui.product_window import SaleWindow
from ui.sale_window import SaleWindow
class MainWindow():
    def __init__ (self,root):
        self.root = root
        self.root.title("Market System")
        self.root.geometry("800x600") #RES

        #cria janela principal
        self.center_window()
        #cria menu
        self.create_menu()
        
        #cria uma "caixa" para organizar elementos
        self.main_frame = ttk.Frame(self.root, padding="20")
        #grade                                        #estica o frame em todas as direções
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N,tk.S))#Norte,SUL,Leste,Oeste

        title = ttk.Label(
                self.main_frame,
                text="Sistema de Gerenciamento de Mercado",
                font=("Arial", 24, "bold")
        )
        title.grid(row=0,column=0, pady=30)

        self.create_buttons()

    def center_window(self):
        self.root.update_idletasks() #faz o tinker processar todas as tarefas pendentes
        width = 800 #Largura
        height = 600 #Altura
        y = (self.root.winfo_screenheight()//2) - (height // 2) # Altura,Largura da tela 
        x = (self.root.winfo_screenwidth() // 2) - (width / 2) # divide por 2 e depos subtrai metade da janela
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        #exemplo               "800x600+560+240"                                      

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        #                                opção de destacar o menu 0/1                                    
        products_menu = tk.Menu(menubar, tearoff=0)#remove a opção de destacar
        #add menu produtos na barra
        menubar.add_cascade(label="Produtos", menu=products_menu)
        products_menu.add_command(label="Cadastrar Produto",command=self.open_product_window)
        products_menu.add_separator()#linha separadora
    
    def create_buttons(self):
        button_frame = ttk.Frame(self.mamin_frame)
        button_frame.grid(row=1, column=0, pady=20) #espaçamento em 20px
        #produtos
        button_products=ttk.Button(
            button_frame,
            text="Gerenciar Produtos",
            comand=self.open_product_window, #Função
            width=30
        )
        
        button_products.grid(row=0,column=0,padx=10,pady=10)

        #vendas
        button_sales = ttk.Button(
            button_frame,
            text="Nova venda",
            command=self.open_sale_window,
            width=30
        )
        button_sales.grid(row=1,column=0, padx=10,pady=10)
        
        #reports
        button_reports = ttk.Button(
            button_frame,
            text="Relatorios",
            command=self.open_report_window,
            widht=20
        )
    # "Gerenciador" de janelas
    def open_product_window(self):
        from ui.product_window import ProductWindow
        ProductWindow(self.root)
    def open_product_list(self):
        from ui.product_window import ProductWindow
        ProductWindow(self.root, mode="list")
    def open_sale_window(self):
        from ui.sale_window import SaleWindow
        SaleWindow(self.root, mode="history")
    def open_report_window(self):
        from ui.report_window import ReportWindow
        ReportWindow(self.root)
