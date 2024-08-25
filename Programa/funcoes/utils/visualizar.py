from Programa.funcoes.utils.formatar import cep, cnpj, cpf, telefone
from Programa.funcoes.utils.separar import separador2, separador3

from Programa.funcoes.crud import buscarPorId

def usuario(usuario, comId = False, comFavoritos = False, comCompras = False, basico = False):
    if comId:
        print(f'ID: ')

    print(f"Nome: {usuario.nome_usuario}")
    print(f"CPF: {cpf(usuario.cpf)}")

    if not basico:
        print(f"Telefone: {telefone(usuario.telefone_usuario)}")
        print(f"Email: {usuario.email_usuario}")
        quantEnderecos = enderecos(usuario.enderecos)

    if comFavoritos:
        quantFavoritos = produtos(usuario.favoritos, favoritados = True)

    if comCompras:
        quantCompras = compras(usuario.compras)

    fechaSeparador = not basico
    if fechaSeparador == True:
        fechaSeparador = quantEnderecos > 0
    if fechaSeparador == False and comFavoritos:
        fechaSeparador = quantFavoritos > 0
    if fechaSeparador == False and comCompras:
        fechaSeparador = quantCompras > 0
    if fechaSeparador:
        print(separador2)

def vendedor(vendedor, comId = False, comProdutos = False, comVendas = False, basico = False):
    if comId:
        print(f'ID: {vendedor.id}')

    print(f"Nome: {vendedor.nome_vendedor}")
    print(f"CNPJ: {cnpj(vendedor.cnpj)}")

    if not basico:
        print(f"Telefone: {telefone(vendedor.telefone_vendedor)}")
        print(f"Email: {vendedor.email_vendedor}")
        quantEnderecos = enderecos(vendedor.enderecos)

    if comProdutos:
        quantProdutos = produtos(vendedor.produtos)

    if comVendas:
        quantVendas = compras(vendedor.vendas, vendidas = True)
        
    fechaSeparador = not basico
    if fechaSeparador == True:
        fechaSeparador = quantEnderecos > 0
    if fechaSeparador == False and comProdutos:
        fechaSeparador = quantProdutos > 0
    if fechaSeparador == False and comVendas:
        fechaSeparador = quantVendas > 0
    if fechaSeparador:
        print(separador2)

def compra(compra, comId = False, comVendedor = False, comUsuario = False):
    if comId:
        print(f'ID: {compra.id}')

    print(f'Data da Compra: {compra.data_compra}')

    if comUsuario:
        usuario_compra = buscarPorId("usuarios", compra.id_cliente)
        if usuario_compra:
            print(separador2)
            print("Cliente:")
            usuario(usuario_compra, basico = True)
        else:
            print("Cliente: Este usuário não existe mais!")

        endereco_usuario = buscarPorId("enderecos", compra.endereco_usuario)
        if endereco_usuario:
            print(separador2)
            print("Local de Destino:")
            endereco(endereco_usuario)
        else:
            print("Local de Destino: este endereço não existe mais!")

    if comVendedor:
        vendedor_compra = buscarPorId("vendedores", compra.id_vendedor)
        if vendedor_compra:        
            print(separador2)
            print("Vendedor:")
            vendedor(vendedorCompra, basico = True)
        else:
            print("Vendedor: Este vendedor não existe mais!")

        endereco_vendedor = buscarPorId("enderecos", compra.endereco_vendedor)
        if endereco_vendedor:
            print(separador2)
            print("Local do Remetente:")
            endereco(compra.endereco_vendedor)
        else:
            print("Local do Remetente: este endereço não existe mais!")

    produtos(compra.produtos)
    print(separador2)

    print("Total:", compra.valor_total)

def produto(produto, comId=False, comVendedor=False):    
    if comId:
        print(f'ID: {str(produto.id)}')
    print(f"Produto: {produto.nome_produto}")
    print(f"Valor: R${produto.valor_produto:.2f}")

    if comVendedor:
        vendedor = buscarPorId("vendedores", produto.id_vendedor)
        
        if vendedor:
            print(separador2)
            vendedor(vendedor, basico=True)
            print(separador2)
        else:
            print("Vendedor: Este vendedor não existe mais!")

def endereco(endereco, comId = False):
    if comId:
        print(f'ID: {endereco.id}')

    print(f'{endereco.rua}, {endereco.numero} ({endereco.descricao}) - {endereco.bairro}')
    print(f'CEP: {cep(endereco.cep)}')
    print(f'{endereco.cidade} - {endereco.estado} ({endereco.pais})')

def enderecos(ids, comId = False):
    if ids == None:
        print("Endereços: Nenhum endereço encontrado")
        return 0
    quantidade = len(ids)
    if quantidade == 0:
        print("Endereços: Nenhum endereço encontrado")
    elif quantidade == 1:
        print(separador2)
        print("Endereço:")
        enderecoDesejado = buscarPorId("enderecos", ids[1])
        if enderecoDesejado:
            print(separador3)
            endereco(enderecoDesejado, comId)
            print(separador3)
        else:
            print("Erro ao procurar por endereço")
    else:
        print(separador2)
        print("Endereços:")
        for id in ids:
            print(separador3)
            enderecoDesejado = buscarPorId("enderecos", id)
            if enderecoDesejado:
                endereco(enderecoDesejado, comId)
            else:
                print("Erro ao procurar por endereço")
        print(separador3)
    return quantidade

def produtos(ids, comId = False, favoritos = False):
    titulo = "Produto" if not favoritos else "Favorito"
    if ids == None:
        print(f"{titulo}: Nenhum {titulo.lower()} encontrado")
        return 0
    quantidade = len(ids)
    if quantidade == 0:
        print(f"{titulo}: Nenhum {titulo.lower()} encontrado")
    elif quantidade == 1:
        print(separador2)
        print(f"{titulo}:")
        produtoDesejado = buscarPorId("produtos", ids[1])
        if produtoDesejado:
            print(separador3)
            produto(produtoDesejado, comId)
            print(separador3)
        else:
            print(f"Erro ao procurar por {titulo.lower()}")
    else:
        print(separador2)
        print(f"{titulo}s:")
        for id in ids:
            print(separador3)
            produtoDesejado = buscarPorId("produtos", id)
            if produtoDesejado:
                produto(produtoDesejado, comId)
            else:
                print(f"Erro ao procurar por {titulo.lower()}")
        print(separador3)
    return quantidade

def compras(ids, comId = False, vendas = False):
    titulo = "Compra" if not vendas else "Venda"
    if ids == None:
        print(f"{titulo}: Nenhuma {titulo.lower()} encontrada")
        return 0
    quantidade = len(ids)
    if quantidade == 0:
        print(f"{titulo}: Nenhuma {titulo.lower()} encontrada")
    elif quantidade == 1:
        print(separador2)
        print(f"{titulo}:")
        produtoDesejado = buscarPorId("compras", ids[1])
        if produtoDesejado:
            print(separador3)
            produto(produtoDesejado, comId)
            print(separador3)
        else:
            print(f"Erro ao procurar por {titulo.lower()}")
    else:
        print(separador2)
        print(f"{titulo}s:")
        for id in ids:
            print(separador3)
            compraDesejado = buscarPorId("compras", id)
            if compraDesejado:
                compra(compraDesejado, comId, vendas, not vendas)
            else:
                print(f"Erro ao procurar por {titulo.lower()}")
        print(separador3)
    return quantidade