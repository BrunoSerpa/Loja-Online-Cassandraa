from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.escolher import vendedor as escolherVendedor
from Programa.funcoes.utils.visualizar import vendedor as visualizarVendedor
from Programa.funcoes.utils.separar import separador1
from Programa.funcoes.crud import cadastrar as cadastrarVendedor, atualizar as atualizarVendedor, buscarPorAtributo, buscarPorId, buscarTodos, excluir as excluirDado
from Programa.funcoes.enderecos import cadastrarMultiplos as cadastrarEnderecos, gerenciar as gerenciarEnderecos
from Programa.funcoes.produtos import cadastrarMultiplos as cadastrarProdutos, gerenciar as gerenciarProdutos
from Programa.funcoes.compras import deletar as deletarVenda

def cadastrar():
    nome = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
    cnpj = entrada("Insira o CNPJ do vendedor", "Cnpj", "CNPJ inválido. deve conter apenas os 14 números")
    email = entrada("Insira o email do vendedor", "Email", "Email inválido. Certifique-se de que contém '@' e '.'")
    telefone = entrada("Insira o telefone do vendedor", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")

    id = cadastrarVendedor("vendedores", ["nome_vendedor", "cnpj", "email_vendedor", "telefone_vendedor"], [nome, cnpj, email, telefone])
    if id:
        print("Vendedor cadastrado com sucesso!")
        if entrada("Deseja cadastra seus enderecos? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
            enderecos_vendedor = cadastrarEnderecos()
            atualizar_enderecos = atualizarVendedor("vendedores", id, ["enderecos"], [enderecos_vendedor])
            if not atualizar_enderecos:
                return
            print("Endereços vinculados com sucesso!")

        if entrada("Deseja cadastra seus produtos? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
            produtos_vendedor = cadastrarProdutos(id)
            atualizar_produtos = atualizarVendedor("vendedores", id, ["produtos"], [produtos_vendedor])
            if not atualizar_produtos:
                return
            print("Produtos vinculados com sucesso!")

def atualizar():
    nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome do vendedor não pode estar em branco")
    vendedores_encontrados = buscarPorAtributo("vendedores", "nome_vendedor", nome_vendedor)
    vendedor = escVendedor(vendedores_encontrados)
    if vendedor:
        while True:
            print(separador1)
            print("Vendedor atual:")
            visualizarVendedor(vendedor, comId = True, comProdutos = True, comVendas = True)
            print(f'{separador1}\n')

            print(separador1)
            print("O que deseja alterar?")
            print(separador2)
            print("1 - Nome")
            print("2 - CNPJ")
            print("3 - Email")
            print("4 - Telefone")
            print("5 - Enderecos")
            print("6 - Produtos")
            print(separador2)
            print("7 - Remover venda")
            print("0 - Salvar e sair")
            print(f'{separador1}\n')

            print("Qual ação deseja realizar?")
            opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma das opções!")
            limparTerminal()

            if opcaoEscolhida == '0':
                atualizar = atualizarVendedor("vendedores", vendedor.id, ["nome_vendedor", "cnpj", "email_vendedor", "telefone_vendedor", "enderecos", "produtos", "vendas"], [vendedor.nome_vendedor, vendedor.cnpj, vendedor.email_vendedor, vendedor.telefone_vendedor, vendedor.enderecos, vendedor.produtos, vendedor.vendas])
                if not atualizar:
                    return
                print("Vendedor atualizado com sucesso!")
                break
            elif opcaoEscolhida == '1':
                vendedor.nome = entrada("Insira o novo nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
            elif opcaoEscolhida == '2':
                vendedor.cnpj = entrada("Insira o novo CNPJ do vendedor", "Cnpj", "CNPJ inválido. deve conter apenas os 14 números")
            elif opcaoEscolhida == '3':                                       
                vendedor.email = entrada("Insira o novo email do vendedor", "Email", "Email inválido. Certifique-se de que contém '@' e '.'")
            elif opcaoEscolhida == '4':
                vendedor.telefone = entrada("Insira o novo telefone do vendedor", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            elif opcaoEscolhida == '5':
                vendedor.enderecos = gerenciarEnderecos(vendedor.enderecos)
            elif opcaoEscolhida == '6':
                vendedor.produtos = gerenciarProdutos(vendedor.produtos, vendedor.id)
            elif opcaoEscolhida == '7':
                deletou = deletarVenda(vendedor)
                if not deletou:
                    continue
                elif not vendedor.produtos:
                    vendedor.produtos = set()
                vendedor.vendas.pop(deletou[0])
                vendedor.produtos += deletou[1]
            else:
                print("Opção inválida!")

def deletar():
    nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome do vendedor não pode estar em branco")
    vendedores_encontrados = buscarPorAtributo("vendedores", "nome_vendedor", nome_vendedor)
    vendedor = escVendedor(vendedores_encontrados)
    if vendedor:
        visualizarVendedor(vendedor, comId = True, comProdutos = True, comVendas = True)
        if entrada("Deseja realmente deletar este vendedor específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
            if vendedor.enderecos:
                for endereco in vendedor.enderecos:
                    deletar = excluirDado("enderecos", endereco)
                    if not deletar:
                        return None
                print("Endereços deletado com sucesso!")
            if vendedor.produtos:
                for produto in vendedor.produtos:
                    deletar = excluirDado("produtos", produto)
                    if not deletar:
                        return None
                print("Produtos deletado com sucesso!")
            deletar = excluirDado("vendedores", id)
            if not deletar:
                return None
            print("Vendedor deletado com sucesso!")
    return id

def listar():
    vendedores = []
    if entrada("Deseja procurar um vendedor específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        ids = buscarPorAtributo("vendedores", "nome_vendedor", entrada("Insira o nome do vendedor", "NaoVazio", "Insira o nome do vendedor"))    
        for id in ids:
            vendedor = buscarPorId("vendedores", id)
            if vendedor:
                vendedores.append(vendedor)
    else:
        vendedores = buscarTodos("vendedores")
    limparTerminal()
    if not vendedores:
        print("Nenhum vendedor encontrado!")
    if len(vendedores) == 0:
        print("Nenhum vendedor encontrado!")
    elif len(vendedores) == 1:
        print(separador1)
        vendedor = buscarPorId("vendedores", vendedores[0])
        visualizarVendedor(vendedor, comProdutos = True, basico = True)
        print(separador1)
    else:
        for numeroVendedor, vendedor in enumerate(vendedores, start = 1):
            print(separador1)
            print(f'{numeroVendedor}º vendedor:')
            visualizarVendedor(vendedor, comProdutos = True, basico = True)
        print(separador1)