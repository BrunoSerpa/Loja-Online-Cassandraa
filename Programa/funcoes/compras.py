from datetime import datetime

from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.escolher import usuario as escolherCliente, endereco as escolherEndereco, vendedor as escolherVendedor, produto as escolherProduto, compra as escolherCompra
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.separar import separador1
from Programa.funcoes.utils.visualizar import compra as visualizarCompra

from Programa.funcoes.crud import buscarPorAtributo, buscarPorId, buscarTodos, cadastrar as cadEndereco, atualizar as atualizarDado, excluir as excCompra


def cadastrar(cliente = None):
    comCliente = False if cliente == None else True
    if not comCliente:
        nome_cliente = entrada("Insira o nome do cliente", "NaoVazio", "Nome não pode estar em branco.")
        clientes = buscarPorAtributo("clientes", "nome_cliente", nome_cliente)
        cliente = escolherCliente(clientes)
        if not cliente:
            return None

    endereco_cliente = escolherEndereco(cliente.enderecos)
    if not endereco_cliente:
        return None

    nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
    vendedores = buscarPorAtributo("vendedores", "nome_vendedor", nome_vendedor)

    vendedor = escolherVendedor(vendedores)
    if not vendedor:
        return None

    endereco_vendedor = escolherEndereco(vendedor.enderecos)
    if not endereco_vendedor:
        return None
    
    produtos_disponiveis = vendedor.produtos
    if not produtos_disponiveis:
        return None

    produtos = set()
    valor_total = 0
    while len(produtos_disponiveis) > 0:
        produto = escolherProduto(produtos_disponiveis)
        if not produto:
            return None
        
        produtos_disponiveis.pop(produto.id)
        produtos.add(produto.id)

        valor_total += float(produto.preco)

        if entrada("Deseja comprar mais algum produto? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
            break

    if not produtos:
        return None

    id = cadastrarCompra("compras", ["data_compra", "id_cliente", "endereco_cliente", "id_vendedor", "endereco_vendedor", "produtos", "valor_total"], [datetime.utcnow(), cliente.id, endereco_cliente.id, vendedor.id, endereco_vendedor.id, produtos, valor_total])

    if id:
        print("Compra cadastrada com sucesso")
        vendedor.vendas.add(id)
        atualizar = atualizarDado("vendedores", vendedor.id, ["vendas", "produtos"], [vendedor.vendas, produtos_disponiveis])
        if not atualizar:
            return None
        print("Vendedor vinculado com sucesso!")

        if comCliente:
            cliente.compras.add(id)
            atualizar = atualizarDado("usuarios", cliente.id, ["compras"], [cliente.compras])
            if not atualizar:
                return None
            print("Cliente vinculado com sucesso!")
    return id

def cadastrarMultiplos(cliente):
    compras = set()
    while True:
        limparTerminal()
        id = cadastrar(cliente)
        if id:
            compras.add(id)

        if entrada("Deseja cadastrar mais alguma compra? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() != 'S':
            break
    return compras

def deletar(vendedor = None):
    comVendedor = False if vendedor == None else True
    if not comVendedor:
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
        vendedores = buscarPorAtributo("vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escolherVendedor(vendedores)
        if not vendedor:
            return None

    compra = escolherCompras(vendedor.compras)
    if not compra:
        return None

    visualizarCompra(compra, True, comVendedor, True)

    if entrada("Deseja realmente deletar esta compra específica? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        cliente = buscarPorId("usuarios", compra.id_cliente)
        if cliente:
            cliente.compras.pop(compra.id)
            atualizar = atualizarDado("usuarios", cliente.id, ["compras"], [cliente.compras])
            if not atualizar:
                return None
            print("Compra removida do cliente!")
            
        if not comVendedor:
            vendedor.produtos += compra.produtos
            atualizar = atualizarDado("vendedores", vendedor.id, ["produtos"], [vendedor.produtos])
            if not atualizar:
                return None
            print("Produtos restaurados ao estoque do vendedor!")

            vendedor.vendas.pop(compra.id)
            atualizar = atualizarDado("vendedores", vendedor.id, ["vendas"], [vendedor.vendas])
            if not atualizar:
                return None
            print("Venda removida do vendedor!")

        excluir = excluirCompra("compras", compra.id)
        if not excluir:
            return None
        print("Compra deletada com sucesso!")

    return [compra.id, compra.produtos]

def listarVendas():
    vendas = []
    if entrada("Deseja procurar vendas de um vendedor específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        vendedores = buscarPorAtributo("vendedores", "nome_vendedor", entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco"))
        vendedor = escolherVendedor(vendedores)
        if vendedor:
            if vendedor.vendas:
                for id in vendedor.vendas:
                    venda = buscarPorId("compras", id)
                    if venda:
                        vendas.append(venda)
    else:
        vendas = buscarTodos("compras")

    limparTerminal()
    if not vendas:
        print("Nenhuma venda encontrada!")
    elif len(vendas) == 0:
        print("Nenhuma venda encontrada!")
    elif len(vendas) == 1:
        print(separador1)        
        visualizarCompra(venda, comUsuario = True)
        print(separador1)
    else:
        for numeroVenda, id in enumerate(vendas, start = 1):
            print(separador1)
            print(f'{numeroVenda - quantError}ª venda:')
            visualizarCompra(venda, comUsuario = True)
        print(separador1)

def listarCompras():
    compras = []
    if entrada("Deseja procurar vendas de um cliente específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        clientes = buscarPorAtributo("clientes", "nome_cliente", entrada("Insira o nome do cliente", "NaoVazio", "Nome não pode estar em branco"))
        cliente = escolherCliente(clientes)
        if cliente:
            if cliente.compras:
                for id in cliente.compras:
                    compra = buscarPorId("compras", id)
                    if compra:
                        compras.append(compra)
    else:
        compras = buscarTodos("compras")

    limparTerminal()
    if not compras:
        print("Nenhuma compra encontrada!")
    elif len(compras) == 0:
        print("Nenhuma compra encontrada!")
    elif len(compras) == 1:
        print(separador1)        
        visualizarCompra(compra, comVendedor = True)
        print(separador1)
    else:
        for numeroCompra, id in enumerate(compras, start = 1):
            print(separador1)
            print(f'{numeroCompra - quantError}ª compra:')
            visualizarCompra(compra, comUsuario = True)
        print(separador1)