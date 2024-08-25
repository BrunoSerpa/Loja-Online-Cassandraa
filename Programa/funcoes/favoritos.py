from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.crud import buscarPorAtributo, buscarPorId
from Programa.funcoes.utils.escolher import produto as escolherFavorito
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.visualizar import produto as visualizarFavorito

def cadastrar(favoritos):
    nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
    produtos = buscarPorAtributo("produtos", "nome_produto", nome_produto)

    produtos_possiveis = set()
    for produto in produtos:
        if not produto in favoritos:
            produtos_possiveis.add(produto)
    favorito = escFavorito(produtos_possiveis)
    if favorito:
        print("Produto favoritado com sucesso!")
        return favorito.id
    return None

def gerenciar(favoritos):
    if not favoritos:
        favoritos = set()

    while True:
        print(separador1)
        print("Favoritos atuais:")
        for id in favoritos:
            favorito = buscarPorId("produtos", id)
            if favorito:
                visualizarFavorito(favorito, comVendedor = True)
            else:
                favoritos.pop(id)
        print(f'{separador1}\n')
        quantidade = len(favoritos)

        print(separador1)
        print("O que deseja fazer?")
        print(separador2)
        print("1 - Adicionar um favorito")
        if quantidade > 0:
            print("2 - Remover um favorito")
        print(separador2)
        print("0 - Salvar e sair")
        print(separador1)
        
        print("\nQual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        if opcaoEscolhida == "0":
            return favoritos
        elif opcaoEscolhida == "1":
            id = cadastrar(favoritos)
            if id:
                favoritos.add(id)
        elif opcaoEscolhida == "2":
            favorito = escFavorito(favoritos, favoritos=True)
            if favorito:
                favoritos.pop(favorito.id)
        else:
            print("Insira uma opção válida.")