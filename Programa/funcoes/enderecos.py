from Programa.funcoes.crud import cadastrar as cadastrarEndereco, atualizar as atualizarEndereco, excluir as excluirEndereco, buscarPorId
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.visualizar import endereco as visualizarEndereco
from Programa.funcoes.utils.escolher import endereco as escolherEndereco

def cadastrar():
    cep = entrada("Insira o CEP", "Cep", "CEP Inválido. Deve conter 8 dígitos numéricos.")
    pais = entrada("Insira o país", "NaoVazio", "País não pode estar em branco.")
    estado = entrada("Insira o estado", "NaoVazio", "Estado não pode estar em branco.")
    cidade = entrada("Insira o cidade", "NaoVazio", "Cidade não pode estar em branco.")
    bairro = entrada("Insira o bairro", "NaoVazio", "Bairro não pode estar em branco.")
    rua = entrada("Insira o rua", "NaoVazio", "Rua não pode estar em branco.")
    numero = entrada("Insira o número", "Numero", "Número não pode estar em branco.")
    descricao = entrada("Insira a descrição", "NaoVazio", "Descrição não pode estar em branco.")

    id = cadastrarEndereco("enderecos", ["cep", "pais", "estado", "cidade", "bairro", "rua", "numero", "descricao"], [cep, pais, estado, cidade, bairro, rua, numero, descricao])
    if id:
        print("Endereço cadastrado com sucesso!")
    return id

def cadastrarMultiplos():
    produtos = set()

    while True:
        limparTerminal()
        id = cadastrar()
        if id:
            produtos.add(id)
        if input("Deseja cadastrar mais algum endereço? (S/N)").upper() != 'S':
            break
    return produtos

def atualizar(endereco):
    while True:
        print(separador1)
        print("Endereço atual:")
        visEndereco(endereco, comId = True)
        print(f'{separador1}\n')

        print(separador1)
        print("O que deseja alterar?")
        print(separador2)
        print("1 - CEP")
        print("2 - País")
        print("3 - Estado")
        print("4 - Cidade")
        print("5 - Bairro")
        print("6 - Rua")
        print("7 - Número")
        print("8 - Descrição")
        print(separador2)
        print("0 - Salvar e sair")
        print(f'{separador1}\n')

        print("Qual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        limparTerminal()

        if opcaoEscolhida == '0':
            atualizar = atualizarEndereco("enderecos", endereco.id, ["cep", "pais", "estado", "cidade", "bairro", "rua", "numero", "descricao"], [endereco.cep, endereco.pais, endereco.estado, endereco.cidade, endereco.bairro, endereco.rua, endereco.numero, endereco.descricao])
            if not atualizar:
                return None
            print("Endereço atualizado com sucesso!")
            break
        elif opcaoEscolhida == '1':
            endereco.cep = entrada("Insira o novo CEP", "Cep", "CEP Inválido. Deve conter 8 dígitos numéricos.")
        elif opcaoEscolhida == '2':
            endereco.pais = entrada("Insira o novo país", "NaoVazio", "País não pode estar em branco.")
        elif opcaoEscolhida == '3':
            endereco.estado = entrada("Insira o novo estado", "NaoVazio", "Estado não pode estar em branco.")
        elif opcaoEscolhida == '4':
            endereco.cidade = entrada("Insira o novo cidade", "NaoVazio", "Cidade não pode estar em branco.")
        elif opcaoEscolhida == '5':
            endereco.bairro = entrada("Insira o novo bairro", "NaoVazio", "Bairro não pode estar em branco.")
        elif opcaoEscolhida == '6':
            endereco.rua = entrada("Insira o novo rua", "NaoVazio", "Rua não pode estar em branco.")
        elif opcaoEscolhida == '7':
            endereco.numero = entrada("Insira o novo número", "Numero", "Número não pode estar em branco.")
        elif opcaoEscolhida == '8':
            endereco.descricao = entrada("Insira a nova descrição", "NaoVazio", "Descrição não pode estar em branco.")
        else:
            print("Insira uma opção válida.")
    return id

def deletar(endereco):
    visEndereco(endereco, comId = True)
    if entrada("Deseja realmente deletar este endereço específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        excluir = excluirEndereco("enderecos", endereco.id)
        if not excluir:
            return None
        print("Endereço deletado com sucesso!")
    return id

def gerenciar(enderecos):
    if not enderecos:
        enderecos = set()
    while True:
        print(separador1)
        print("Endereços atuais:")
        for id in enderecos:
            endereco = buscarPorId("enderecos", id)
            if endereco:
                visEndereco(endereco, comId = True)
            else:
                enderecos.pop(id)
        print(f'{separador1}\n')
        quantidade = len(enderecos)
            
        print(separador1)
        print("O que deseja fazer?")
        print(separador2)
        print("1 - Adicionar endereço")
        if quantidade > 0:
            print("2 - Atualizar endereço")
            print("3 - Deletar endereço")
        print(separador2)
        print("0 - Salvar e sair")
        print(f'{separador1}\n')
        
        print("Qual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")

        if opcaoEscolhida == "0":
            return enderecos
        elif opcaoEscolhida == "1":
            endereco = cadastrar()
            enderecos.add(endereco)
        elif opcaoEscolhida == "2" and quantidade > 0:
            endereco = escEndereco(enderecos)
            if endereco:
                atualizar(endereco)
        elif opcaoEscolhida == "3"  and quantidade > 0:
            endereco = escEndereco(enderecos)
            if endereco:
                deletar(endereco)
                enderecos.pop(endereco.id)
        else:
            print("Insira uma opção válida.")