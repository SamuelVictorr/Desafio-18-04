#programa feito por Samuel Victor, Enrico Reno e José Miguel; Turma: ADS 2025.1
#favor, ler o arquivo "ABRAME" antes de ver o programa por inteiro.


import gestao_estoque_cozinha as cozinha
import gestao_pedidos as pedidos
import gestao_pagamentos as pagamentos

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("SISTEMA DE GERENCIAMENTO DE RESTAURANTE".center(40))
        print("="*40)
        print("[1] Gestão de Estoque")
        print("[2] Gestão de Cardápio")
        print("[3] Gestão de Pedidos")
        print("[4] Gestão de Pagamentos")
        print("[5] Sair")
        print("="*40)
        
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Digite um número válido!")
            continue
            
        if opcao == 1:
            cozinha.menu_estoque()
        elif opcao == 2:
            cozinha.menu_cardapio()
        elif opcao == 3:
            pedidos.menu_pedidos()
        elif opcao == 4:
            pagamentos.menu_pagamento()
        elif opcao == 5:
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    #dados iniciais para teste (opcional, caso não queira, remova-os))
    cozinha.cadastrar_produto(1, "Arroz", 10, "kg", 5.0, "30/12/2023")
    cozinha.cadastrar_produto(2, "Feijão", 8, "kg", 8.0, "15/01/2024")
    cozinha.cadastrar_item_cardapio("Prato Feito", "Arroz, feijão e carne", 25.0, {"Arroz": 0.2, "Feijão": 0.1})
    
    menu_principal()