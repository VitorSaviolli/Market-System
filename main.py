import tkinter as tk
from ui.main_window import MainWindow

if __name__ == "__main__":
    #cria janela principal
    root = tk.TK()
    app = MainWindow(root)
    #para manter a janela aberta, funciona como debug também
    root.amainloop()