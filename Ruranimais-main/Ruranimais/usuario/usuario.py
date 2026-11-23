# Imports
from funcoes.util import cursor


class Usuario:
    def __init__(self, nome_usuario, email, cpf, senha, id):
        self.nome_usuario = nome_usuario
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.id = id

 # Transforma a linha do banco (id, nome, email, senha, cpf) em um Usuario
    @classmethod
    def from_tupla(cls, dados):
        return cls(nome_usuario=dados[1], email=dados[2], cpf=dados[4], senha=dados[3], id=dados[0])

    # Procura um usuário pelo id (devolve None se não existir)
    @classmethod
    def procurar_id(cls, id):
        cursor.execute("SELECT * FROM usuarios_ruranimais WHERE id = ?", (id,))
        dados = cursor.fetchone()
        return cls.from_tupla(dados) if dados else None

    # Procura um usuário pelo nome (devolve None se não existir)
    @classmethod
    def procurar_nome_usuario(cls, nome_usuario):
        cursor.execute("SELECT * FROM usuarios_ruranimais WHERE nome_usuario = ?", (nome_usuario,))
        dados = cursor.fetchone()
        return cls.from_tupla(dados) if dados else None

# Mensagens ficam em mensagem.py e postagens em postagem.py