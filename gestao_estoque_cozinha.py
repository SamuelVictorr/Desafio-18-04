import datetime

estoque = []
cardapio = {}
pedidos_cozinha = []

def cadastrar_produto(codigo, nome, quantidade, unidade, preco_unitario, validade):
    produto = {
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "unidade": unidade,
        "preco_unitario": preco_unitario,
        "validade": datetime.datetime.strptime(validade, "%d/%m/%Y")
    }
    estoque.append(produto)
    return True, f"Produto {nome} cadastrado com sucesso!"

def consultar_estoque():
    return estoque

def imprimir_estoque():
    print("\n--- ESTOQUE ---")
    print(f"{'Código':<10} {'Nome':<20} {'Quantidade':<15} {'Preço':<10}")
    for produto in estoque: # olha cada produto no estoque, depois imprime os daddos
        print(f"{produto['codigo']:<10} {produto['nome']:<20} {produto['quantidade']:>5} {produto['unidade']:<8} R${produto['preco_unitario']:<8.2f}")

def atualizar_estoque(codigo, nova_quantidade):
    for produto in estoque:
        if produto["codigo"] == codigo: # procura o produto pelo código fornecido, para realizar a atualização
            produto["quantidade"] = nova_quantidade
            return True, f"Estoque de {produto['nome']} atualizado."
    return False, "Produto não encontrado."

def alertas_estoque():
    hoje = datetime.datetime.today()
    alertas = []
    for produto in estoque: # Vê se o estoque de produtos e gerar alertas, pela quantidade do produto e pela data de validade
        if produto["quantidade"] < 5:
            alertas.append(f"ALERTA: Estoque baixo de {produto['nome']} ({produto['quantidade']} {produto['unidade']})")
        dias_para_validade = (produto["validade"] - hoje).days
        if dias_para_validade <= 3:
            alertas.append(f"ALERTA: {produto['nome']} vence em {dias_para_validade} dias ({produto['validade'].strftime('%d/%m/%Y')})")
    return alertas if alertas else ["Nenhum alerta no estoque."]

def cadastrar_item_cardapio(nome, descricao, preco, ingredientes):
    cardapio[nome] = {
        "descricao": descricao,
        "preco": preco,
        "ingredientes": ingredientes
    }
    return True, f"Item {nome} cadastrado no cardápio!"

def imprimir_cardapio(): # imprime o cardápio, com os ingredientes e preços
    print("\n--- CARDÁPIO ---")
    for nome, info in cardapio.items():
        print(f"\n{nome} - {info['descricao']} (R${info['preco']:.2f})")
        print("Ingredientes:")
        for ing, qtd in info["ingredientes"].items():
            print(f"  - {ing}: {qtd}")

def verificar_ingredientes(prato):
    if prato not in cardapio:
        return False, "Prato não encontrado no cardápio."
    
    for nome_ing, qtd_necessaria in cardapio[prato]["ingredientes"].items(): # Olha se o prato tem os ingredientes necessários e se o estoque tem o suficiente
        ingrediente_encontrado = False
        for produto in estoque:
            if produto["nome"] == nome_ing:
                ingrediente_encontrado = True
                if produto["quantidade"] < qtd_necessaria:
                    return False, f"Estoque insuficiente de {nome_ing}"
                break
        if not ingrediente_encontrado:
            return False, f"Ingrediente {nome_ing} não encontrado no estoque."
    return True, "Ingredientes disponíveis."

def registrar_pedido(cliente, prato, mesa):
    disponivel, msg = verificar_ingredientes(prato)
    if not disponivel:
        return False, msg
    
    # Baixa estoque
    for nome_ing, qtd_necessaria in cardapio[prato]["ingredientes"].items():
        for produto in estoque:
            if produto["nome"] == nome_ing:
                produto["quantidade"] -= qtd_necessaria
                break
    
    pedido = {
        "cliente": cliente,
        "prato": prato,
        "mesa": mesa,
        "status": "recebido",
        "horario": datetime.datetime.now()
    }
    pedidos_cozinha.append(pedido) # Adiciona o pedido na lista de pedidos da cozinha
    return True, f"Pedido de {prato} para {cliente} (Mesa {mesa}) registrado."

def menu_estoque():
    while True:
        print("\n" + "="*40)
        print("GERENCIAMENTO DE ESTOQUE".center(40))
        print("="*40)
        print("[1] Cadastrar produto")
        print("[2] Consultar estoque")
        print("[3] Atualizar estoque")
        print("[4] Ver alertas")
        print("[5] Voltar")
        print("="*40)
        
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Digite um número válido!")
            continue
            
        if opcao == 1:
            codigo = int(input("Código: "))
            nome = input("Nome: ")
            quantidade = float(input("Quantidade: "))
            unidade = input("Unidade (kg, g, l, etc): ")
            preco = float(input("Preço unitário: "))
            validade = input("Data de validade (dd/mm/aaaa): ")
            sucesso, msg = cadastrar_produto(codigo, nome, quantidade, unidade, preco, validade)
            print(msg)
            
        elif opcao == 2:
            imprimir_estoque()
            
        elif opcao == 3:
            imprimir_estoque()
            codigo = int(input("\nCódigo do produto: "))
            nova_quantidade = float(input("Nova quantidade: "))
            sucesso, msg = atualizar_estoque(codigo, nova_quantidade)
            print(msg)
            
        elif opcao == 4:
            alertas = alertas_estoque()
            for alerta in alertas:
                print(alerta)
                
        elif opcao == 5:
            break
            
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")

def menu_cardapio():
    while True:
        print("\n" + "="*40)
        print("GERENCIAMENTO DE CARDÁPIO".center(40))
        print("="*40)
        print("[1] Cadastrar item")
        print("[2] Consultar cardápio")
        print("[3] Atualizar item")
        print("[4] Voltar")
        print("="*40)
        
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Digite um número válido!")
            continue
            
        if opcao == 1:
            nome = input("Nome do prato: ")
            descricao = input("Descrição: ")
            preco = float(input("Preço: "))
            
            print("\nCadastro de ingredientes:")
            imprimir_estoque()
            ingredientes = {}
            while True:
                nome_ing = input("\nNome do ingrediente (ou deixe em branco para terminar): ")
                if not nome_ing:
                    break
                qtd = float(input(f"Quantidade de {nome_ing}: "))
                ingredientes[nome_ing] = qtd
            
            sucesso, msg = cadastrar_item_cardapio(nome, descricao, preco, ingredientes)
            print(msg)
            
        elif opcao == 2:
            imprimir_cardapio()
            
        elif opcao == 3:
            imprimir_cardapio()
            nome = input("\nNome do prato para atualizar: ")
            if nome not in cardapio:
                print("Prato não encontrado!")
                continue
                
            nova_desc = input(f"Nova descrição (atual: {cardapio[nome]['descricao']}): ")
            novo_preco = input(f"Novo preço (atual: {cardapio[nome]['preco']:.2f}): ")
            
            if nova_desc:
                cardapio[nome]["descricao"] = nova_desc
            if novo_preco:
                cardapio[nome]["preco"] = float(novo_preco)
            
            print("Prato atualizado com sucesso!")
            
        elif opcao == 4:
            break
            
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")