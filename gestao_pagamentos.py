#import gestao_cozinha
#import gestao_de_pedidos
import datetime

"""
Módulo: gestao_pagamentos.py
Descrição: Gestão de contas, pagamentos e relatórios para restaurante
Única biblioteca utilizada: datetime

"""

from datetime import datetime

#estruturação dos dados em listas ou dicionários: 

contas = {}          # {mesa: {"pedidos": [], "clientes": int, "status": str}}
pagamentos = []       # [{"mesa": int, "valor": float, "forma": str, "data": datetime}]
relatorios_diarios = {}  # {data_str: {"total": float, "pratos_vendidos": {item: int}}}

# ---------- funções das contas ----------
def abrir_conta(mesa, num_clientes):
    #abre uma conta nova pro cliente/clientes
    if mesa in contas and contas[mesa]["status"] == "aberta":
        return False, f"Já existe conta aberta para a mesa {mesa}"
    
    contas[mesa] = {
        "pedidos": [],
        "clientes": num_clientes,
        "status": "aberta"
    }
    return True, f"Conta aberta para mesa {mesa} com {num_clientes} cliente(s)"

def adicionar_pedido(mesa, nome_pedido, valor_pedido):
    #adiciona um pedido à conta da mesa
    if mesa not in contas:
        return False, f"Mesa {mesa} não encontrada"
    if contas[mesa]["status"] != "aberta":
        return False, f"Conta da mesa {mesa} está fechada"
    
    contas[mesa]["pedidos"].append({
        "item": nome_pedido,
        "valor": valor_pedido
    })
    return True, f"Pedido '{nome_pedido}' adicionado à mesa {mesa}"

def calcular_total_conta(mesa):
    #calcula o valor total da conta da mesa
    if mesa not in contas:
        return 0, f"Mesa {mesa} não encontrada"
    
    total = sum(p["valor"] for p in contas[mesa]["pedidos"])
    return total, f"Total da mesa {mesa}: R${total:.2f}"

def dividir_conta(mesa):
    #divide o valor da conta igualmente entre os clientes
    total, msg = calcular_total_conta(mesa)
    if total == 0:
        return 0, msg
    
    num_clientes = contas[mesa]["clientes"]
    valor_por_cliente = total / num_clientes
    return valor_por_cliente, f"Valor por cliente: R${valor_por_cliente:.2f}"

def aplicar_taxa_servico(mesa, percentual=10):
    #aplica taxa de serviço à conta da mesa
    total, msg = calcular_total_conta(mesa)
    if total == 0:
        return 0, msg
    
    taxa = total * (percentual / 100)
    total_com_taxa = total + taxa
    return total_com_taxa, f"Total com taxa: R${total_com_taxa:.2f}"

# ---------- Funções de Pagamento ----------
def registrar_pagamento(mesa, valor_pago, forma_pagamento, valor_entregue=None):
    #registra o pagamento e fecha a conta
    if mesa not in contas:
        return False, f"Mesa {mesa} não encontrada"
    
    total, _ = calcular_total_conta(mesa)
    if total == 0:
        return False, "Conta sem pedidos registrados"
    
    # Atualiza relatório diário
    data_atual = datetime.now().strftime("%d/%m/%Y")
    if data_atual not in relatorios_diarios:
        relatorios_diarios[data_atual] = {"total": 0, "pratos_vendidos": {}}
    
    relatorios_diarios[data_atual]["total"] += valor_pago
    
    #contabiliza os pratos vendidos
    for pedido in contas[mesa]["pedidos"]:
        item = pedido["item"]
        if item in relatorios_diarios[data_atual]["pratos_vendidos"]:
            relatorios_diarios[data_atual]["pratos_vendidos"][item] += 1
        else:
            relatorios_diarios[data_atual]["pratos_vendidos"][item] = 1
    
    #registrando os pagamentos
    pagamentos.append({
        "mesa": mesa,
        "valor": valor_pago,
        "forma": forma_pagamento,
        "data": datetime.now()
    })
    
    #fecha a conta
    contas[mesa]["status"] = "fechada"
    
    #calcula o troco
    mensagem_troco = ""
    if forma_pagamento.lower() == "dinheiro" and valor_entregue:
        troco = valor_entregue - valor_pago
        mensagem_troco = f" Troco: R${troco:.2f}"
    
    return True, f"Pagamento registrado. Mesa {mesa} fechada.{mensagem_troco}"

# ---------- funções dos relatórios ----------
def gerar_relatorio_diario(data=None):
    #gera o relatório de vendas da data atual
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")
    
    if data not in relatorios_diarios:
        return {}, f"Nenhuma venda registrada em {data}"
    
    relatorio = relatorios_diarios[data]
    
    #ordena itens por quantidade
    itens_ordenados = sorted(
        relatorio["pratos_vendidos"].items(),
        key=lambda item: item[1],
        reverse=True
    )
    
    #prepara dados do relatório
    dados_relatorio = {
        "data": data,
        "total_vendas": relatorio["total"],
        "itens_mais_vendidos": itens_ordenados[:5]  # Top 5 itens
    }
    
    return dados_relatorio, "Relatório gerado com sucesso"

def calcular_media_mesas():
    #calcula o valor médio gasto por mesa
    if not pagamentos:
        return 0, "Nenhum pagamento registrado"
    
    #agrupa pagamentos por mesa
    total_por_mesa = {}
    for pagamento in pagamentos:
        mesa = pagamento["mesa"]
        if mesa in total_por_mesa:
            total_por_mesa[mesa] += pagamento["valor"]
        else:
            total_por_mesa[mesa] = pagamento["valor"]
    
    num_mesas = len(total_por_mesa)
    total_geral = sum(total_por_mesa.values())
    media = total_geral / num_mesas
    
    return media, f"Média por mesa: R${media:.2f} (total {num_mesas} mesas)"

# ---------- funções auxiliares ----------
def listar_contas_abertas():
    #receber informações de uma mesa ainda em atendimento
    contas_abertas = [
        (mesa, info["clientes"]) 
        for mesa, info in contas.items() 
        if info["status"] == "aberta"
    ]
    return contas_abertas, "Contas abertas listadas"

def listar_pedidos_mesa(mesa):
    #retorna os pedidos de uma mesa que você pediu
    if mesa not in contas:
        return [], f"Mesa {mesa} não encontrada"
    
    pedidos = contas[mesa]["pedidos"]
    return pedidos, f"Pedidos da mesa {mesa} listados"

def obter_historico_pagamentos():
    #retorna os pagamentos registrados
    return pagamentos, "Histórico de pagamentos"