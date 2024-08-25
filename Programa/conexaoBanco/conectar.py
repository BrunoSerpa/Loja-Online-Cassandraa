from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement

from Programa.conexaoBanco.configuracao import configuracao, tabelas
from Programa.funcoes.utils.salvarErro import salvarErro

def conectar():
    try:
        configNuvem, idCliente, segredoCliente = configuracao()
        provedorAutenticacao = PlainTextAuthProvider(idCliente, segredoCliente)
        cluster = Cluster(cloud=configNuvem, auth_provider=provedorAutenticacao)
        sessao = cluster.connect()
        sessao.execute("USE mercado;")
        for query in tabelas():
            try:
                sessao.execute(query)
            except Exception as e:
                salvarErro("Erro ao criar tabela", e)
        return sessao
    except Exception as e:
        salvarErro("Erro ao conectar ao Cassandra", e)
        return None