import gestao_cozinha 
mesas = []

def cadastrar_mesa():
    try:
        numero = int(input("Número da mesa: "))
        for mesa in mesas:
            if mesa["numero da mesa"] == numero:
                print("Mesa já registrada.")
                return

        capacidade = int(input("Capacidade: "))
        statu = input("Status (livre, ocupada, reservada): ").strip().lower()
        if statu not in ["livre", "ocupada", "reservada"]:
            print("Status inválido.")
            return
        
        m = {
            "numero da mesa": numero,
            "capacidade": capacidade,
            "status": statu
        }
        mesas.append(m)
        print("Mesa cadastrada.")
    except:
        print("Erro nos dados da mesa.")

def listar_mesas():
    for m in mesas:
        print(f"Mesa {m['numero da mesa']} - Capacidade: {m['capacidade']} - Status: {m['status']}")

def ocupar_mesa():
    listar_mesas()
    numero = int(input("Número da mesa para ocupar: "))
    for m in mesas:
        if m["numero da mesa"] == numero:
            if m["status"] != "livre":
                print("Mesa não está livre.")
                return
            m["status"] = "ocupada"
            print("Mesa ocupada.")
            return
    print("Mesa não encontrada.")

def liberar_mesa():
    listar_mesas()
    numero = int(input("Número da mesa para liberar: "))
    for m in mesas:
        if m["numero da mesa"] == numero:
            m["status"] = "livre"
            print("Mesa liberada.")
            return
    print("Mesa não encontrada.")

def fazer_pedido():
    cliente = input("Nome do cliente: ")
    prato = input("Prato desejado: ")
    mesa = int(input("Número da mesa: "))
    gestao_cozinha.registrar_pedido(cliente, prato, mesa)


while True:
    print("\nGestão de Pedidos")
    print("1 - Cadastrar mesa")
    print("2 - Listar mesas")
    print("3 - Ocupar mesa")
    print("4 - Liberar mesa")
    print("5 - Fazer pedido")
    print("6 - Sair")

    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Digite um número válido.")
        continue

    match opcao:
        case 1:
            cadastrar_mesa()
        case 2:
            listar_mesas()
        case 3:
            ocupar_mesa()
        case 4:
            liberar_mesa()
        case 5:
            fazer_pedido()
        case 6:
            break
        case _:
            print("Opção inválida!")