class empresa:
    def __init__(self, 
                 CNPJ:str=None, 
                 nome:str=None
                ):
        self.set_CNPJ(CNPJ)
        self.set_nome(nome)

    def set_CNPJ(self, CNPJ:str):
        self.CNPJ = CNPJ

    def set_nome(self, nome:str):
        self.nome = nome

    def get_CNPJ(self) -> str:
        return self.CNPJ

    def get_nome(self) -> str:
        return self.nome

    def to_string(self) -> str:
        return f"CNPJ: {self.get_CNPJ()} | Nome: {self.get_nome()}"
