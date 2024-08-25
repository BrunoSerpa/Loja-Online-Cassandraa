from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.salvarErro import salvarErro
from Programa.funcoes.utils.separar import separador1
import Programa.funcoes.utils.visualizar as visualizar

from Programa.funcoes.crud import buscarPorId

def visualizar_item(tipo, **kwargs):
    funcoes_disponiveis = [attr for attr in dir(visualizar) if callable(getattr(visualizar, attr)) and not attr.startswith('__')]

    if tipo in funcoes_disponiveis:
        funcao_visualizar = getattr(visualizar, tipo)
        funcao_visualizar(**kwargs)
    else:
        salvarErro("Erro ao buscar função", f"A função de visualização '{tipo}' não existe no módulo 'visualizar'. Funções disponíveis: {', '.join(funcoes_disponiveis)}")

def escolher_item(tipo, ids, descricao, tipo_visualizar, **kwargs):
    quantidade = len(ids)
    if quantidade == 0:
        print(f"Nenhuma {descricao} encontrada" if not kwargs.get('termo_feminino') else f"Nenhum {descricao} encontrado")
    elif quantidade == 1:
        item = buscarPorId(tipo, ids[0])
        if item:
            return item
    else:
        print(f"Mais de uma {descricao} encontrada!" if kwargs.get('termo_feminino') else f"Mais de um {descricao} encontrado!")
        itens = []
        while True:
            print(f"Escolha uma {descricao}:" if kwargs.get('termo_feminino') else f"Escolha um {descricao}:")
            quantError = 0
            for posicao, id in enumerate(ids, start=1):
                item = buscarPorId(tipo, id)
                if item:
                    print(separador1)
                    print(f'{posicao - quantError} - {tipo.capitalize()}:')
                    visualizar_item(tipo_visualizar, item, **kwargs)
                    print(separador1)

                    itens.append(item)
                else:
                    quantError += 1
                    print(f"Erro ao procurar id: {id}")

            posicao = int(entrada("Insira a opção desejada", "Numero", "Insira uma opção válida."))
            limparTerminal()

            if 0 < posicao <= len(itens):
                return itens[posicao - 1]
            elif len(itens) == 0:
                return None
            else:
                print("Insira uma opção existente.")
    return None

def usuario(usuarios):
    if not usuarios:
        print("Nenhum usuário correspondente encontrado!")
        return None
    return escolher_item("usuarios", usuarios, "usuário", 'usuario', comId = True)

def vendedor(vendedores):
    if not vendedores:
        print("Nenhum vendedor correspondente encontrado!")
        return None
    return escolher_item("vendedores", vendedores, "vendedor", 'vendedor', comId = True, comProdutos = True)

def endereco(enderecos):
    if not enderecos:
        print("Nenhum endereco correspondente encontrado!")
        return None
    return escolher_item("enderecos", enderecos, "endereço", 'endereco', comId = True)

def produto(produtos, favoritos = False):
    descricao = "favorito" if favoritos else "produto"
    if not produtos:
        print(f"Nenhum {descricao} correspondente encontrado!")
        return None
    return escolher_item("produtos", produtos, descricao, 'produto', comId = True, favoritos = favoritos)

def compra(compras, vendas = False):
    descricao = "compra" if not vendidas else "venda"
    if not compras:
        print(f"Nenhuma {descricao} correspondente encontrada!")
        return None
    return escolher_item("compras", compras, descricao, 'compra', comId = True, comUsuario = not vendas, comVendedor = vendas, termo_feminino = True)