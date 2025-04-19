import datetime
import gestao_estoque_cozinha as cozinha

mesas = []

def cadastrar_mesa():
    try:
        numero = int(input("Número da mesa: "))
        for mesa in mesas: # Olha cada mesa na lista measas, e vê se o número já cadastrado
            if mesa["numero"] == numero:
                print("Mesa já registrada.")
                return False
            
        capacidade = int(input("Capacidade: "))
        status = input("Status (livre/ocupada/reservada): ").lower()
        
        if status not in ["livre", "ocupada", "reservada"]: # Vê se o status é válido
            print("Status inválido!")
            return False
            
        mesa = {
            "numero": numero,
            "capacidade": capacidade,
            "status": status,
            "clientes": None,
            "pedidos": []
        }
        mesas.append(mesa)
        print(f"Mesa {numero} cadastrada com sucesso!")
        return True
        
    except ValueError:
        print("Erro: Digite valores numéricos para número e capacidade.")
        return False

def listar_mesas():
    if not mesas:
        print("Nenhuma mesa cadastrada.")
        return
    
    print("\n--- MESAS ---")
    print(f"{'Número':<10} {'Capacidade':<12} {'Status':<15} {'Clientes':<20}")
    for mesa in mesas:
        clientes = mesa["clientes"] if mesa["clientes"] else "-" # Se tiver clientes cadastrados, mostra os nomes se não, mostra "-"
        print(f"{mesa['numero']:<10} {mesa['capacidade']:<12} {mesa['status']:<15} {clientes:<20}")

def ocupar_mesa():
    listar_mesas()
    try:
        numero = int(input("\nNúmero da mesa para ocupar: "))
        for mesa in mesas:
            if mesa["numero"] == numero:
                if mesa["status"] != "livre":
                    print("Mesa não está disponível para ocupação.")
                    return False
                    
                clientes = input("Nome dos clientes: ")
                mesa["status"] = "ocupada"
                mesa["clientes"] = clientes
                print(f"Mesa {numero} ocupada por {clientes}.")
                return True
                
        print("Mesa não encontrada.")
        return False
        
    except ValueError:
        print("Digite um número válido.")
        return False

def liberar_mesa():
    listar_mesas()
    try:
        numero = int(input("\nNúmero da mesa para liberar: "))
        for mesa in mesas:
            if mesa["numero"] == numero: # Olha se a mesa existe
                if mesa["status"] == "livre": 
                    print("Mesa já está livre.")
                    return False
                    
                mesa["status"] = "livre"
                mesa["clientes"] = None
                print(f"Mesa {numero} liberada.")
                return True
                
        print("Mesa não encontrada.")
        return False
        
    except ValueError:
        print("Digite um número válido.")
        return False

def fazer_pedido():
    listar_mesas()
    try:
        numero = int(input("\nNúmero da mesa: "))
        
        # Verifica se mesa foi cadastrada e se está ocupada
        mesa_encontrada = None
        for mesa in mesas:
            if mesa["numero"] == numero:
                mesa_encontrada = mesa
                break
                
        if not mesa_encontrada:
            print("Mesa não encontrada.")
            return False
            
        if mesa_encontrada["status"] != "ocupada":
            print("Mesa não está ocupada.")
            return False
            
        cozinha.imprimir_cardapio()
        prato = input("\nPrato desejado: ")
        
        # Verifica se prato existe
        if prato not in cozinha.cardapio:
            print("Prato não encontrado no cardápio.")
            return False
            
        # Registra pedido na cozinha
        sucesso, msg = cozinha.registrar_pedido(mesa_encontrada["clientes"], prato, numero)
        if not sucesso:
            print(msg)
            return False
            
        # Registra pedido na mesa
        mesa_encontrada["pedidos"].append({
            "prato": prato,
            "hora": datetime.datetime.now(),
            "status": "pendente"
        })
        
        print(f"Pedido de {prato} registrado para mesa {numero}.")
        return True
        
    except ValueError:
        print("Digite um número válido.")
        return False

def menu_pedidos():
    while True:
        print("\n" + "="*40)
        print("GERENCIAMENTO DE PEDIDOS".center(40))
        print("="*40)
        print("[1] Cadastrar mesa")
        print("[2] Listar mesas")
        print("[3] Ocupar mesa")
        print("[4] Liberar mesa")
        print("[5] Fazer pedido")
        print("[6] Voltar")
        print("="*40)
        
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Digite um número válido!")
            continue
            
        if opcao == 1:
            cadastrar_mesa()
        elif opcao == 2:
            listar_mesas()
        elif opcao == 3:
            ocupar_mesa()
        elif opcao == 4:
            liberar_mesa()
        elif opcao == 5:
            fazer_pedido()
        elif opcao == 6:
            break
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")