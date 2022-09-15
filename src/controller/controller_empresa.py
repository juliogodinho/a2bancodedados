from model.empresa import empresa
from conexion.oracle_queries import OracleQueries

class Controller_empresa:
    def __init__(self):
        pass
        
    def inserir_empresa(self) -> empresa:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CNPJ
        cnpj = input("CNPJ (Novo): ")

        if self.verifica_existencia_empresa(oracle, cnpj):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Insere e persiste a nova empresa
            oracle.write(f"insert into empresa values ('{cnpj}', '{nome}')")
            # Recupera os dados da nova empresa criado transformando em um DataFrame
            df_empresa = oracle.sqlToDataFrame(f"select cnpj, nome from empresa where cnpj = '{cnpj}'")
            # Cria um novo objeto empresa
            novo_empresa = empresa(df_empresa.cpf.values[0], df_empresa.nome.values[0])
            # Exibe os atributos do novo cliente
            print(novo_empresa.to_string())
            # Retorna o objeto novo_empresa para utilização posterior, caso necessário
            return novo_empresa
        else:
            print(f"O CNPJ {cnpj} já está cadastrado.")
            return None

    def atualizar_empresa(self) -> empresa:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da empresa a ser alterada
        cnpj = int(input("CNPJ da empresa que deseja alterar o nome: "))

        # Verifica se a empresa existe na base de dados
        if not self.verifica_existencia_empresa(oracle, cnpj):
            # Solicita a nova descrição da empresa
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome da empresa existente
            oracle.write(f"update empresa set nome = '{novo_nome}' where cnpj = {cnpj}")
            # Recupera os dados do nova empresa criada transformando em um DataFrame
            df_empresa = oracle.sqlToDataFrame(f"select cnpj, nome from empresa where cnpj = {cnpj}")
            # Cria um novo objeto empresa
            empresa_atualizado = empresa(df_empresa.cpf.values[0], df_empresa.nome.values[0])
            # Exibe os atributos da nova empresa
            print(empresa_atualizado.to_string())
            # Retorna o objeto empresa_atualizado para utilização posterior, caso necessário
            return empresa_atualizado
        else:
            print(f"O CNPJ {cnpj} não existe.")
            return None

    def excluir_empresa(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CNPJ da empresa a ser alterado
        cnpj = int(input("CNPJ da empresa que irá excluir: "))        

        # Verifica se a empresa existe na base de dados
        if not self.verifica_existencia_empresa(oracle, cnpj):            
            # Recupera os dados da nova empresa criada transformando em um DataFrame
            df_empresa = oracle.sqlToDataFrame(f"select cnpj, nome from empresa where cnpj = {cnpj}")
            # Revome a empresa da tabela
            oracle.write(f"delete from empresa where cnpj = {cnpj}")            
            # Cria um novo objeto empresa para informar que foi removido
            empresa_excluido = empresa(df_empresa.cpf.values[0], df_empresa.nome.values[0])
            # Exibe os atributos da empresa excluída
            print("Empresa Removida com Sucesso!")
            print(empresa_excluido.to_string())
        else:
            print(f"O CNPJ {cnpj} não existe.")

    def verifica_existencia_empresa(self, oracle:OracleQueries, cnpj:str=None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_empresa = oracle.sqlToDataFrame(f"select cnpj, nome from clientes where cnpj = {cnpj}")
        return df_empresa.empty
