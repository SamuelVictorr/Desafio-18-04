from datetime import datetime

contas = {}
pagamentos = []
relatorios_diarios = {}

def abrir_conta(mesa, clientes): # abrir conta da mesa
    if mesa in contas and contas[mesa]["status"] == "aberta":
        return False, f"Já existe conta aberta para a mesa {mesa}"
    
    contas[mesa] = {
        "pedidos": [],
        "clientes": clientes,
        "status": "aberta",
        "taxas": {
            "garcom": 2.50,
            "federal": 0.0,
            "estadual": 0.0
        }
    }
    return True, f"Conta aberta para mesa {mesa} com {clientes} cliente(s)"

def adicionar_pedido_conta(mesa, item, valor): # adicionar pedido à conta da mesa
    if mesa not in contas:
        return False, f"Mesa {mesa} não encontrada"
    if contas[mesa]["status"] != "aberta":
        return False, f"Conta da mesa {mesa} está fechada"
    
    contas[mesa]["pedidos"].append({
        "item": item,
        "valor": valor,
        "hora": datetime.now()
    })
    return True, f"Pedido '{item}' adicionado à mesa {mesa}"

def calcular_total_conta(mesa):
    if mesa not in contas:
        return 0, f"Mesa {mesa} não encontrada"
    
    subtotal = sum(p["valor"] for p in contas[mesa]["pedidos"]) # soma os valores dos pedidos
    garcom = contas[mesa]["taxas"]["garcom"]
    federal = subtotal * 0.057
    estadual = subtotal * 0.033
    
    total = subtotal + garcom + federal + estadual
    
    contas[mesa]["taxas"]["federal"] = federal
    contas[mesa]["taxas"]["estadual"] = estadual
    
    return total, f"Total da mesa {mesa}: R${total:.2f}"

def aplicar_taxas(mesa): # aplica taxas à conta da mesa
    total, msg = calcular_total_conta(mesa)
    if total == 0:
        return 0, msg
    
    detalhes = (
        f"\n--- CONTA MESA {mesa} ---\n"
        f"Subtotal: R${sum(p['valor'] for p in contas[mesa]['pedidos']):.2f}\n"
        f"Taxa garçom: R${contas[mesa]['taxas']['garcom']:.2f}\n"
        f"Imposto Federal (5.7%): R${contas[mesa]['taxas']['federal']:.2f}\n"
        f"Imposto Estadual (3.3%): R${contas[mesa]['taxas']['estadual']:.2f}\n"
        f"TOTAL: R${total:.2f}"
    )
    
    return total, detalhes

def dividir_conta(mesa): # divide o total da conta entre os clientes
    if mesa not in contas:
        return 0, f"Mesa {mesa} não encontrada"
    
    total, _ = calcular_total_conta(mesa)
    num_clientes = contas[mesa]["clientes"] # número de clientes na mesa
    valor_por_cliente = total / num_clientes
    
    return valor_por_cliente, f"Valor por cliente ({num_clientes}): R${valor_por_cliente:.2f}"

def registrar_pagamento(mesa, forma_pagamento, valor_entregue=None): # registra o pagamento da conta
    if mesa not in contas:
        return False, f"Mesa {mesa} não encontrada"
    
    total, _ = calcular_total_conta(mesa)
    
    # Atualiza relatório diário
    data_atual = datetime.now().strftime("%d/%m/%Y")
    if data_atual not in relatorios_diarios:
        relatorios_diarios[data_atual] = {"total": 0, "itens_vendidos": {}}
    
    relatorios_diarios[data_atual]["total"] += total
    
    # Contabiliza itens vendidos
    for pedido in contas[mesa]["pedidos"]:
        item = pedido["item"]
        if item in relatorios_diarios[data_atual]["itens_vendidos"]:
            relatorios_diarios[data_atual]["itens_vendidos"][item] += 1
        else:
            relatorios_diarios[data_atual]["itens_vendidos"][item] = 1
    
    # Registra pagamento
    pagamento = {
        "mesa": mesa,
        "valor": total,
        "forma": forma_pagamento,
        "data": datetime.now(),
        "troco": 0
    }
    
    # Calcula troco se for em dinheiro
    if forma_pagamento.lower() == "dinheiro" and valor_entregue:
        if valor_entregue < total:
            return False, f"Valor insuficiente. Faltam R${total - valor_entregue:.2f}"
        pagamento["troco"] = valor_entregue - total
    
    pagamentos.append(pagamento)
    contas[mesa]["status"] = "fechada"
    
    # Prepara mensagem
    msg = f"Pagamento registrado para mesa {mesa}. Total: R${total:.2f}"
    if pagamento["troco"] > 0:
        msg += f" | Troco: R${pagamento['troco']:.2f}"
    
    return True, msg

def gerar_relatorio_diario(data=None):
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")
    
    if data not in relatorios_diarios:
        return None, f"Nenhuma venda registrada em {data}" # vê se há vendas nesse dia
    
    relatorio = relatorios_diarios[data] # pega o relatório do dia
    itens_ordenados = sorted(
        relatorio["itens_vendidos"].items(),
        key=lambda item: item[1],
        reverse=True
    )
    
    return {
        "data": data,
        "total": relatorio["total"],
        "top_itens": itens_ordenados[:5]
    }, "Relatório gerado com sucesso"

def menu_pagamento():
    while True:
        print("\n" + "="*40)
        print("GERENCIAMENTO DE PAGAMENTOS".center(40))
        print("="*40)
        print("[1] Abrir conta")
        print("[2] Adicionar pedido à conta")
        print("[3] Calcular total")
        print("[4] Aplicar taxas")
        print("[5] Dividir conta")
        print("[6] Registrar pagamento")
        print("[7] Relatório diário")
        print("[8] Voltar")
        print("="*40)
        
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Digite um número válido!")
            continue
            
        if opcao == 1:
            mesa = int(input("Número da mesa: "))
            clientes = int(input("Número de clientes: "))
            sucesso, msg = abrir_conta(mesa, clientes)
            print(msg)
            
        elif opcao == 2:
            mesa = int(input("Número da mesa: "))
            item = input("Nome do pedido: ")
            valor = float(input("Valor: "))
            sucesso, msg = adicionar_pedido_conta(mesa, item, valor)
            print(msg)
            
        elif opcao == 3:
            mesa = int(input("Número da mesa: "))
            total, msg = calcular_total_conta(mesa)
            print(msg)
            
        elif opcao == 4:
            mesa = int(input("Número da mesa: "))
            total, detalhes = aplicar_taxas(mesa)
            print(detalhes)
            
        elif opcao == 5:
            mesa = int(input("Número da mesa: "))
            valor, msg = dividir_conta(mesa)
            print(msg)
            
        elif opcao == 6:
            mesa = int(input("Número da mesa: "))
            forma = input("Forma de pagamento (dinheiro/cartão): ")
            
            if forma.lower() == "dinheiro":
                valor = float(input("Valor entregue: "))
                sucesso, msg = registrar_pagamento(mesa, forma, valor)
            else:
                sucesso, msg = registrar_pagamento(mesa, forma)
            
            print(msg)
            
        elif opcao == 7:
            data = input("Data (dd/mm/aaaa) ou deixe em branco para hoje: ")
            relatorio, msg = gerar_relatorio_diario(data if data else None)
            
            print(msg)
            if relatorio:
                print(f"\n--- RELATÓRIO {relatorio['data']} ---")
                print(f"Total vendido: R${relatorio['total']:.2f}")
                print("\nItens mais vendidos:")
                for item, qtd in relatorio['top_itens']:
                    print(f"- {item}: {qtd}x")
                    
        elif opcao == 8:
            break
            
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")