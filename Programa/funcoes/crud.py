from uuid import uuid4, UUID
from cassandra.query import SimpleStatement

from Programa.conexaoBanco.conectar import conectar
from Programa.funcoes.utils.salvarErro import salvarErro

sessao = conectar()

def cadastrar(colecao, nomes, dados):
    if len(nomes) != len(dados):
        salvarErro("A quantidade de nomes e dados fornecidos são diferentes", f'{len(nomes)} nomes e {len(dados)} dados fornecidos')
        return None
    
    tipos = ', '.join(nomes)
    placeholders = ', '.join(["%s"] * len(dados))
    id = uuid4()
    
    try:
        query = f"INSERT INTO {colecao} (id, {tipos}) VALUES ({id}, {placeholders})"
        prepared_stmt = SimpleStatement(query)
        sessao.execute(prepared_stmt, (id, *dados))
    except Exception as e:
        salvarErro("Erro ao cadastrar registro", e)
        return None
    return id

def atualizar(colecao, id, nomes, dados):
    if len(nomes) != len(dados):
        salvarErro("A quantidade de nomes e dados fornecidos são diferentes", f'{len(nomes)} nomes e {len(dados)} dados fornecidos')
        return None
    try:
        for posicao in range(len(dados)):
            query = f"UPDATE {colecao} SET {nomes[posicao]} = %s WHERE id = {id}"
            prepared_stmt = SimpleStatement(query)
            sessao.execute(prepared_stmt, (dados[posicao]))
    except Exception as e:
        salvarErro("Erro ao atualizar registro", e)
        return None
    return id

def excluir(colecao, id):
    try:
        query = f"DELETE FROM {colecao} WHERE id = {id}"
        prepared_stmt = SimpleStatement(query)
        sessao.execute(prepared_stmt, (id))
    except Exception as e:
        salvarErro("Erro ao deletar registro", e)
        return None
    return id

def buscarTodos(colecao):
    try:
        query = f"SELECT * FROM {colecao}"
        resultados = sessao.execute(query)
        return [row for row in resultados]
    except Exception as e:
        salvarErro("Erro ao buscar todos os registros", e)
        return None

def buscarPorId(colecao, id):
    try:
        query = f"SELECT * FROM {colecao} WHERE id = %s"
        prepared_stmt = SimpleStatement(query)
        resultado = sessao.execute(prepared_stmt, (id)).one()
        if resultado:
            return resultado
        else:
            salvarErro("Registro não encontrado", f'ID {id} não encontrado na coleção {colecao}')
            return None
    except Exception as e:
        salvarErro("Erro ao buscar registro por ID", e)
        return None

def buscarPorAtributo(colecao, nomeCampo, atributo):
    try:
        atributo = f"%{atributo}%"
        
        query = f"SELECT * FROM {colecao} WHERE {nomeCampo} LIKE %s"
        prepared_stmt = SimpleStatement(query)
        resultados = sessao.execute(prepared_stmt, (atributo))
        return [row for row in resultados]
    except Exception as e:
        salvarErro("Erro ao buscar registro por atributo semelhante", e)
        return None

def desconectar():
    sessao.shutdown()