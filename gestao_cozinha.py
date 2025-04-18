"""
Módulo: gestao_cozinha.py
Descrição: Responsável pela gestão de estoque, cardápio e preparo de pratos.
Este sistema é parte de um restaurante para melhorar da gestão
"""

import datetime

# ---------- Estoque ----------
estoque = []

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

def consultar_estoque():
    return estoque

def imprimir_estoque():
    for p in estoque:
        print(p)

def atualizar_estoque(codigo, nova_quantidade):
    for produto in estoque:
        if produto["codigo"] == codigo:
            produto["quantidade"] = nova_quantidade
            print(f"Produto {produto['nome']} atualizado.")
            return
    print("Produto não encontrado.")

def alertas():
    hoje = datetime.datetime.today()
    for produto in estoque:
        if produto["quantidade"] < 5:
            print(f"ALERTA: Estoque baixo do produto '{produto['nome']}'")
        dias_para_validade = (produto["validade"] - hoje).days
        if dias_para_validade <= 3:
            print(f"ALERTA: Produto '{produto['nome']}' próximo da validade ({produto['validade'].strftime('%d/%m/%Y')})")

# ---------- Cardápio ----------
cardapio = {}

def cadastrar_item_cardapio(nome, descricao, preco, ingredientes):
    cardapio[nome] = {
        "descricao": descricao,
        "preco": preco,
        "ingredientes": ingredientes
    }

def consultar_cardapio():
    return cardapio

def imprimir_cardapio():
    for nome, info in cardapio.items():
        print(f"{nome} - {info['descricao']} (R${info['preco']:.2f})")
        print("  Ingredientes:")
        for ing, qtd in info["ingredientes"].items():
            print(f"    {ing}: {qtd}")

def atualizar_item_cardapio(nome, descricao=None, preco=None, ingredientes=None):
    if nome in cardapio:
        if descricao: cardapio[nome]["descricao"] = descricao
        if preco: cardapio[nome]["preco"] = preco
        if ingredientes: cardapio[nome]["ingredientes"] = ingredientes
        print(f"Item '{nome}' atualizado com sucesso.")
    else:
        print("Item não encontrado no cardápio.")

# ---------- Preparo de Pratos e Pedidos ----------
pedidos = [
    {"cliente": "jose","prato": "carne","Numero da Mesa" : 4,"status": "recebido","horario": "10:40"}
        ]

def verificar_ingredientes(prato):
    if prato not in cardapio:
        print("Prato não encontrado no cardápio.")
        return False
    ingredientes = cardapio[prato]["ingredientes"]
    for nome_ing, qtd_necessaria in ingredientes.items():
        encontrado = False
        for produto in estoque:
            if produto["nome"] == nome_ing:
                encontrado = True
                if produto["quantidade"] < qtd_necessaria:
                    print(f"Estoque insuficiente para '{nome_ing}'")
                    return False
        if not encontrado:
            print(f"Ingrediente '{nome_ing}' não encontrado no estoque.")
            return False
    return True

def baixar_estoque(prato):
    ingredientes = cardapio[prato]["ingredientes"]
    for nome_ing, qtd_necessaria in ingredientes.items():
        for produto in estoque:
            if produto["nome"] == nome_ing:
                produto["quantidade"] -= qtd_necessaria


def registrar_pedido(cliente, prato):
    if prato not in cardapio:
        print("Prato não existe no cardápio.")
        return
    if not verificar_ingredientes(prato):
        print("Pedido não pode ser registrado por falta de ingredientes.")
        return
    pedido = {
        "cliente": cliente,
        "prato": prato,
        "status": "recebido",
        "horario": datetime.datetime.now()
    }
    pedidos.append(pedido)
    baixar_estoque(prato)
    print(f"Pedido registrado para {cliente}: {prato}")

def fila_pedidos():
    for idx, pedido in enumerate(pedidos):
        print(f"{idx + 1}. {pedido['cliente']} - {pedido['prato']} ({pedido['status']})")

def atualizar_status_pedido(indice, novo_status):
    if 0 <= indice < len(pedidos):
        pedidos[indice]["status"] = novo_status
        print(f"Status do pedido de {pedidos[indice]['cliente']} atualizado para '{novo_status}'.")
    else:
        print("Pedido não encontrado.")