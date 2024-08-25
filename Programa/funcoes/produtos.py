from Programa.funcoes.crud import cadastrar as cadastrarProduto, atualizar as atualizarDado, excluir as excluirProduto, buscarPorAtributo, buscarPorId, buscarTodos
from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.escolher import vendedor as escolherVendedor, produto as escolherProduto
from Programa.funcoes.utils.separar import separador1, separador2
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.visualizar import produto as visualizarProduto

def cadastrar(id = None):
    comVendedor = False if id == None else True
    if not comVendedor:
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
        vendedores = buscarPorAtributo("vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escVendedor(vendedores)
        if not vendedor:
            return None
        id = vendedor.id

    nome = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco")
    valor = entrada("Insira o valor do produto (exemplo: 1.23)", "Float", 'Valor Inválido. Deve conter apenas o número decimal, separando por ".".')

    id_produto = cadastrarProduto("produtos", ["nome_produto", "valor_produto", "id_vendedor"], [nome, valor, id])
    if not id_produto:
        return None

    print("Produto cadastrado com sucesso!")
    if not comVendedor:
        if not vendedor.produtos:
            vendedor.produtos = set()
        vendedor.produtos.add(id_produto)
        atualizar = atualizarDado("vendedores", id, ["produtos"], [vendedor.produtos])

        if not atualizar:
            excluirProduto("produtos", id_produto)
            return None
        print("Vendedor vinculado com sucesso!")
    return id_produto
   
def cadastrarMultiplos(id):
    produtos = set()
    while True:
        limparTerminal()
        id_produto = cadastrar(id)
        if id_produto:
            produtos.add(id_produto)
        if input("Deseja cadastrar mais algum produto? (S/N)").upper() != 'S':
            break
    return produtos

def atualizar(produto = None):
    if not produto:
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("produtos", "nome_produto", nome_produto)
        produto = escProduto(produtos)
        if not produto:
            return None
        vendedor = buscarPorId("vendedores", produto.id_vendedor)
        if not vendedor:
            return None
        elif not vendedor.produtos:
            print("Este produto já foi vendido, não podendo ser alterado!")
            return None
        elif not produto.id in vendedor.produtos:
            print("Este produto já foi vendido, não podendo ser alterado!")
            return None

    while True:
        print(separador1)
        print("Produto atual:")
        visualizarProduto(produto, True)
        print(f'{separador1}\n')

        print(separador1)
        print("O que deseja alterar?")
        print(separador2)
        print("1 - Nome")
        print("2 - Preço")
        print(separador2)
        print("0 - Salvar e sair")
        print(f'{separador1}\n')

        print("Qual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        limparTerminal()
        if opcaoEscolhida == '0':
            atualizar = crud.atualizar("produtos", id, ["nome_produto", "valor_produto"], [produto.nome_produto, produto.valor_produto])      
            if not atualizar:
                return None
            print("Produto atualizado com sucesso!")
            break
        elif opcaoEscolhida == '1':
            produto.nome_produto = entrada("Insira o novo nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        elif opcaoEscolhida == '2':
            produto.valor_produto = entrada("Insira o novo valor do produto", "Float", "Valor Inválido. Deve conter apenas o número decimal.")
        else:
            print("Insira uma opção válida.")
    return produto.id

def deletar(produto = None):
    comVendedor = True if produto == None else False
    if not produto:
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("produtos", "nome_produto", nome_produto)
        produto = escProduto(produtos)
        if not produto:
            return None

    visualizarProduto(produto, True, comVendedor)
    if entrada("Deseja realmente deletar este produto específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        if comVendedor:
            vendedor = buscarPorId("vendedores", produto.id_vendedor)
            if not vendedor:
                return None
            elif not vendedor.produtos:
                print("Este produto foi vendido, não podendo ser deletado!")
                return None
            elif not produto.id in vendedor.produtos:
                print("Este produto foi vendido, não podendo ser deletado!")
                return None

            vendedor.produtos.pop(id_produto)
            atualizar = atualizarDado("vendedores", id, ["produtos"], [vendedor.produtos])
            if not atualizar:
                return None
            print("Produto removido do vendedor!")

        excluir = excluirProduto("produtos", produto.id)
        if not excluir:
            return None
        print("Produto deletado com sucesso!")

    return id

def listar():
    produtos = []
    if entrada("Deseja procurar um produto específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        ids = crud.buscarPorAtributo("produtos", "nome_produto", nome_produto)
        for id in ids:
            produto = buscarPorId("produtos", id)
            if produto:
                produtos.append(produto)
    else:
        produtos = buscarTodos("produtos")

    if not produtos:
        print("Nenhum produto encontrado!")
    elif len(produtos) == 0:
        print("Nenhum produto encontrado!")
    elif len(produtos) == 1:
        print(separador1)
        visualizarProduto(produto, comVendedor = True)
        print(separador1)
    else:
        for numeroProduto, produto in enumerate(produtos, start = 1):
            print(separador1)
            print(f'{numeroProduto}º produto:')
            visualizarProduto(produto, comVendedor = True)
        print(separador1)

def gerenciar(produtos, id_vendedor):
    if not produtos:
        produtos = set()

    while True:
        print(separador1)
        print("Produtos atuais:")
        for id in produtos:
            produto = buscarPorId("produtos", id)
            if produto:
                visualizarProduto(produto, comId = True)
            else:
                produtos.pop(id)
        print(f'{separador1}\n')
        quantidade = len(produtos)
            
        print(separador1)
        print("O que deseja fazer?")
        print(separador2)
        print("1 - Adicionar um produto")
        if quantidade > 0:
            print("2 - Atualizar um produto")
            print("3 - Deletar um produto")
        print(separador2)
        print("0 - Salvar e sair")
        print(separador1)
        
        print("\nQual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        if opcaoEscolhida == "0":
            return produtos
        elif opcaoEscolhida == "1":
            produto = cadastrar(id_vendedor)
            produtos.add(produto)
        elif opcaoEscolhida == "2" and quantidade > 0:
            produto = escProduto(produtos)
            if produto:
                atualizar(produto)
        elif opcaoEscolhida == "3" and quantidade > 0:
            produto = escProduto(produtos)
            if produto:
                deletar(produto)
                produtos.pop(produto.id)
        else:
            print("Insira uma opção válida.")