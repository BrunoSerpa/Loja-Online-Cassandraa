from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.separar import separador1
from Programa.funcoes.utils.escolher import usuario as escolherUsuario
from Programa.funcoes.utils.visualizar import usuario as visualizarUsuario
from Programa.funcoes.crud import cadastrar as cadastrarUsuario, atualizar as atualizarUsuario, buscarPorAtributo, buscarPorId,  buscarTodos, excluir as excluirDado
from Programa.funcoes.enderecos import cadastrarMultiplos as cadastrarEnderecos, gerenciar as gerenciarEnderecos
from Programa.funcoes.favoritos import gerenciar as gerenciarFavoritos
from Programa.funcoes.compras import cadastrarMultiplos as cadastrarCompras

def cadastrar():
    nome = entrada("Insira o nome do usuário", "NaoVazio", "Nome não pode estar em branco.")
    cpf = entrada("Insira o CPF do usuário", "Cpf", "CPF inválido. deve conter apenas os 11 números")
    email = entrada("Insira o email do usuário", "Email", "Email inválido. Certifique-se de que contém '@' e '.'")
    telefone = entrada("Insira o telefone do usuário", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")

    id = cadastrarUsuario("usuarios", ["nome_usuario", "cpf", "email_usuario", "telefone_usuario"], [nome, cpf, email, telefone])
    if id:
        print("Usuário cadastrado com sucesso!")
        if entrada("Deseja cadastra seus endereços? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
            enderecos_usuario = cadastrarEnderecos()
            atualizar_enderecos = atualizarUsuario("usuarios", id, ["enderecos"], [enderecos_usuario])
            if not atualizar_enderecos:
                return
            print("Endereços vinculados com sucesso!")

def atualizar():
    nome_usuario = entrada("Insira o nome do usuário", "NaoVazio", "Nome do usuário não pode estar em branco")
    usuarios_encontrados = buscarPorAtributo("usuarios", "nome_usuario", nome_usuario)
    usuario = escUsuario(usuarios_encontrados)
    if usuario:
        while True:
            print(separador1)
            print("Usuário atual:")
            visualizarUsuario(usuario, comId = True, comFavoritos = True, comVendas = True)
            print(f'{separador1}\n')

            print(separador1)
            print("O que deseja alterar?")
            print(separador2)
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Email")
            print("4 - Telefone")
            print("5 - Enderecos")
            print("6 - Produtos")
            print(separador2)
            print("7 - Adicionar compras")
            print("0 - Salvar e sair")
            print(f'{separador1}\n')

            print("Qual ação deseja realizar?")
            opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma das opções!")
            limparTerminal()

            if opcaoEscolhida == '0':
                atualizar = atualizarUsuario("usuarios", usuario.id, ["nome_usuario", "cnpj", "email_usuario", "telefone_usuario", "enderecos", "produtos", "vendas"], [usuario.nome_usuario, usuario.cnpj, usuario.email_usuario, usuario.telefone_usuario, usuario.enderecos, usuario.produtos, usuario.vendas])
                if not atualizar:
                    return
                print("Usuario atualizado com sucesso!")
                break
            elif opcaoEscolhida == '1':
                usuario.nome = entrada("Insira o novo nome do usuário", "NaoVazio", "Nome não pode estar em branco.")
            elif opcaoEscolhida == '2':
                usuario.cpF = entrada("Insira o novo CPF do usuário", "Cpf", "CPF inválido. deve conter apenas os 11 números")
            elif opcaoEscolhida == '3':                                       
                usuario.email = entrada("Insira o novo email do usuário", "Email", "Email inválido. Certifique-se de que contém '@' e '.'")
            elif opcaoEscolhida == '4':
                usuario.telefone = entrada("Insira o novo telefone do usuário", "Telefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            elif opcaoEscolhida == '5':
                usuario.enderecos = gerenciarEnderecos(usuario.enderecos)
            elif opcaoEscolhida == '6':
                usuario.favoritos = gerenciarFavoritos(usuario.favoritos)
            elif opcaoEscolhida == '7':
                compras = cadastrarCompras(usuario)
                if not compras:
                    continue
                if not usuario.compras:
                    usuario.compras = set()
                usuario.compras += compras
            else:
                print("Opção inválida!")

def deletar():
    nome_usuario = entrada("Insira o nome do usuário", "NaoVazio", "Nome do usuário não pode estar em branco")
    usuarios_encontrados = buscarPorAtributo("usuarios", "nome_usuario", nome_usuario)
    usuario = escUsuario(usuarios_encontrados)
    if usuario:
        visualizarUsuario(usuario, comId = True, comProdutos = True, comVendas = True)
        if entrada("Deseja realmente deletar este usuário específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
            if usuario.enderecos:
                for endereco in usuario.enderecos:
                    deletar = excluirDado("enderecos", endereco)
                    if not deletar:
                        return
                print("Endereços deletado com sucesso!")
            if usuario.produtos:
                for produto in usuario.produtos:
                    deletar = excluirDado("produtos", produto)
                    if not deletar:
                        return
                print("Produtos deletado com sucesso!")
            deletar = excluirDado("usuarios", usuario.id)
            if not deletar:
                return
            print("Usuario deletado com sucesso!")

def listar():
    usuarios = []
    if entrada("Deseja procurar um usuario específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        ids = buscarPorAtributo("usuarios", "nome_usuario", entrada("Insira o nome do usuario", "NaoVazio", "Insira o nome do usuario"))
        for id in ids:
            usuario = buscarPorId("usuarios", id)
            if usuario:
                usuarios.append(usuario)
    else:
        usuarios = buscarTodos("usuarios")
    limparTerminal()
    if not usuarios:
        print("Nenhum usuário encontrado!")
    elif len(usuarios) == 0:
        print("Nenhum usuário encontrado!")
    elif len(usuarios) == 1:
        print(separador1)
        visualizarUsuario(usuario, basico = True)
        print(separador1)
    else:
        for numeroUsuario, usuario in enumerate(usuarios, start = 1):
            print(separador1)
            print(f'{numeroUsuario}º usuário:')
            visualizarUsuario(usuario, basico = True)
        print(separador1)