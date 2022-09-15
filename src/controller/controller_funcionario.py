from model.funcionario import funcionario
from conexion.oracle_queries import OracleQueries

class Controller_funcionario:
    def __init__(self):
        pass
        
    def inserir_funcionario(self) -> funcionario:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_funcionario(oracle, cpf):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Insere e persiste o novo funcionario
            oracle.write(f"insert into funcionario values ('{cpf}', '{nome}')")
            # Recupera os dados do novo funcionario criado transformando em um DataFrame
            df_funcionario = oracle.sqlToDataFrame(f"select cpf, nome from funcionario where cpf = '{cpf}'")
            # Cria um novo objeto funcionario
            novo_funcionario = funcionario(df_funcionario.cpf.values[0], df_funcionario.nome.values[0])
            # Exibe os atributos do novo funcionario
            print(novo_funcionario.to_string())
            # Retorna o objeto novo_funcionario para utilização posterior, caso necessário
            return novo_cliente
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_funcionario(self) -> funcionario:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do funcionario a ser alterado
        cpf = int(input("CPF do funcionario que deseja alterar o nome: "))

        # Verifica se o funcionario existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):
            # Solicita a nova descrição do funcionario
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome do funcionario existente
            oracle.write(f"update funcionario set nome = '{novo_nome}' where cpf = {cpf}")
            # Recupera os dados do novo funcionario criado transformando em um DataFrame
            df_funcionario = oracle.sqlToDataFrame(f"select cpf, nome from funcionario where cpf = {cpf}")
            # Cria um novo objeto funcionario
            funcionario_atualizado = funcionario(df_funcionario.cpf.values[0], df_funcionario.nome.values[0])
            # Exibe os atributos do novo funcionario
            print(funcionario_atualizado.to_string())
            # Retorna o objeto funcionario_atualizado para utilização posterior, caso necessário
            return funcionario_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_funcionario(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF do funcionario a ser alterado
        cpf = int(input("CPF do funcionario que irá excluir: "))        

        # Verifica se o funcionario existe na base de dados
        if not self.verifica_existencia_funcionario(oracle, cpf):            
            # Recupera os dados do novo funcionario criado transformando em um DataFrame
            df_funcionario = oracle.sqlToDataFrame(f"select cpf, nome from funcionario where cpf = {cpf}")
            # Revome o funcionario da tabela
            oracle.write(f"delete from funcionario where cpf = {cpf}")            
            # Cria um novo objeto funcionario para informar que foi removido
            funcionario_excluido = funcionario(df_funcionario.cpf.values[0], df_funcionario.nome.values[0])
            # Exibe os atributos do funcionario excluído
            print("Funcionario Removido com Sucesso!")
            print(funcionario_excluido.to_string())
        else:
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_funcionario(self, oracle:OracleQueries, cpf:str=None) -> bool:
        # Recupera os dados do novo funcionario criado transformando em um DataFrame
        df_funcionario = oracle.sqlToDataFrame(f"select cpf, nome from funcionario where cpf = {cpf}")
        return df_funcionario.empty
