"""
Sistema de Gerenciamento de Mercado
Projeto para prática de Python
"""

def menu_principal():
    """Exibe o menu principal do sistema"""
    print("\n" + "="*50)
    print("  SISTEMA DE GERENCIAMENTO DE MERCADO")
    print("="*50)
    print("\n1. Gerenciar Produtos")
    print("2. Gerenciar Clientes")
    print("3. Realizar Venda")
    print("4. Relatórios")
    print("5. Sair")
    print("-"*50)

def main():
    """Função principal do sistema"""
    while True:
        menu_principal()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n[Gerenciar Produtos - Em desenvolvimento]")
        elif opcao == "2":
            print("\n[Gerenciar Clientes - Em desenvolvimento]")
        elif opcao == "3":
            print("\n[Realizar Venda - Em desenvolvimento]")
        elif opcao == "4":
            print("\n[Relatórios - Em desenvolvimento]")
        elif opcao == "5":
            print("\nSaindo do sistema... Até logo!")
            break
        else:
            print("\n❌ Opção inválida! Tente novamente.")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()
