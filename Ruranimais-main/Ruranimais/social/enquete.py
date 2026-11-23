# Imports
from funcoes.util import conexao, cursor


# Opção da enquete com a quantidade de votos que ela recebeu
class OpcaoEnquete:
    def __init__(self, texto, id=None, votos=0):
        self.id = id
        self.texto = texto
        self.votos = votos


# Enquete
class Enquete:
    MINIMO_OPCOES = 2
    MAXIMO_OPCOES = 6
    TAMANHO_MAXIMO_OPCAO = 50


    def __init__(self, postagem_id):
        self.postagem_id = postagem_id


    # Cria tabelas da enquete se ainda não existirem
    @staticmethod
    def criar_tabelas():
        cursor.execute(''' CREATE TABLE IF NOT EXISTS opcoes_enquete (
                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       postagem_id INTEGER NOT NULL,
                       texto TEXT NOT NULL,
                       FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE)
        ''')
        # Cada pessoa tem só 1 voto por enquete
        cursor.execute(''' CREATE TABLE IF NOT EXISTS votos_enquete (
                       usuario_id INTEGER NOT NULL,
                       postagem_id INTEGER NOT NULL,
                       opcao_id INTEGER NOT NULL,
                       PRIMARY KEY (usuario_id, postagem_id),
                       FOREIGN KEY (usuario_id) REFERENCES usuarios_ruranimais(id) ON DELETE CASCADE,
                       FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE,
                       FOREIGN KEY (opcao_id) REFERENCES opcoes_enquete(id) ON DELETE CASCADE)
        ''')
        conexao.commit()


    # Confere se texto pode virar opção 
    @staticmethod
    def validar_opcao(texto, opcoes_ja_digitadas):
        if len(texto) > Enquete.TAMANHO_MAXIMO_OPCAO:
            return False, f"A opção pode ter no máximo {Enquete.TAMANHO_MAXIMO_OPCAO} caracteres"
        if texto.casefold() in [opcao.casefold() for opcao in opcoes_ja_digitadas]:
            return False, "Essa opção já foi adicionada"
        return True, "Opção válida"


    # Guarda as opções da enquete no banco
    def criar(self, textos_das_opcoes):
        for texto in textos_das_opcoes:
            cursor.execute(
                "INSERT INTO opcoes_enquete (postagem_id, texto) VALUES (?, ?)",
                (self.postagem_id, texto),
            )
        conexao.commit()


    # Procura as opções com a contagem de votos de cada uma
    def procurar_opcoes(self):
        cursor.execute(
            '''SELECT o.id, o.texto, COUNT(v.usuario_id)
               FROM opcoes_enquete o
               LEFT JOIN votos_enquete v ON v.opcao_id = o.id
               WHERE o.postagem_id = ?
               GROUP BY o.id
               ORDER BY o.id''',
            (self.postagem_id,),
        )
        return [OpcaoEnquete(linha[1], linha[0], linha[2]) for linha in cursor.fetchall()]


    # Qual opção votada? (devolve id da opção ou None)
    def voto_de(self, usuario_id):
        cursor.execute(
            "SELECT opcao_id FROM votos_enquete WHERE usuario_id = ? AND postagem_id = ?",
            (usuario_id, self.postagem_id),
        )
        linha = cursor.fetchone()
        return linha[0] if linha else None


    # Vota (votar na mesma opção de novo tira o voto, votar em outra troca o voto)
    def votar(self, usuario_id, opcao_id):
        voto_atual = self.voto_de(usuario_id)
        if voto_atual == opcao_id:
            cursor.execute(
                "DELETE FROM votos_enquete WHERE usuario_id = ? AND postagem_id = ?",
                (usuario_id, self.postagem_id),
            )
        elif voto_atual is None:
            cursor.execute(
                "INSERT INTO votos_enquete (usuario_id, postagem_id, opcao_id) VALUES (?, ?, ?)",
                (usuario_id, self.postagem_id, opcao_id),
            )
        else:
            cursor.execute(
                "UPDATE votos_enquete SET opcao_id = ? WHERE usuario_id = ? AND postagem_id = ?",
                (opcao_id, usuario_id, self.postagem_id),
            )
        conexao.commit()


    # Soma os votos de todas as opções
    @staticmethod
    def total_votos(opcoes):
        return sum(opcao.votos for opcao in opcoes)