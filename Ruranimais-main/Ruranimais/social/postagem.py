# Imports
from funcoes.util import conexao, cursor
from social.enquete import Enquete


# Comentário em postagem
class Comentario:
    def __init__(self, autor_nome, texto, data):
        self.autor_nome = autor_nome
        self.texto = texto
        self.data = data


# Postagem
class Postagem:
    # Pega postagem + nome do autor + pontos + qtd de comentários + qtd de opções da enquete
    _SELECT = '''SELECT p.id, p.autor_id, u.nome_usuario, p.titulo, p.texto, p.data,
                        (SELECT COALESCE(SUM(valor), 0) FROM votos WHERE postagem_id = p.id),
                        (SELECT COUNT(*) FROM comentarios WHERE postagem_id = p.id),
                        (SELECT COUNT(*) FROM opcoes_enquete WHERE postagem_id = p.id)
                 FROM postagens p
                 JOIN usuarios_ruranimais u ON u.id = p.autor_id'''


    def __init__(self, autor_id, titulo, texto="", id=None, data=None,
                 autor_nome=None, pontos=0, qtd_comentarios=0, tem_enquete=False):
        self.id = id
        self.autor_id = autor_id
        self.titulo = titulo
        self.texto = texto
        self.data = data
        self.autor_nome = autor_nome
        self.pontos = pontos
        self.qtd_comentarios = qtd_comentarios
        self.tem_enquete = tem_enquete
        # ^ True se tem enquete


    # Cria tabelas do feed se ainda não existirem
    @staticmethod
    def criar_tabelas():
        cursor.execute(''' CREATE TABLE IF NOT EXISTS postagens (
                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       autor_id INTEGER NOT NULL,
                       titulo TEXT NOT NULL,
                       texto TEXT NOT NULL DEFAULT '',
                       data TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                       FOREIGN KEY (autor_id) REFERENCES usuarios_ruranimais(id) ON DELETE CASCADE)
        ''')
        cursor.execute(''' CREATE TABLE IF NOT EXISTS comentarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       postagem_id INTEGER NOT NULL,
                       autor_id INTEGER NOT NULL,
                       texto TEXT NOT NULL,
                       data TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                       FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE,
                       FOREIGN KEY (autor_id) REFERENCES usuarios_ruranimais(id) ON DELETE CASCADE)
        ''')
        # valor = 11 (disli (like) ou -ke), só 1 voto por pessoa na enquete
        cursor.execute(''' CREATE TABLE IF NOT EXISTS votos (
                       usuario_id INTEGER NOT NULL,
                       postagem_id INTEGER NOT NULL,
                       valor INTEGER NOT NULL,
                       PRIMARY KEY (usuario_id, postagem_id),
                       FOREIGN KEY (usuario_id) REFERENCES usuarios_ruranimais(id) ON DELETE CASCADE,
                       FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE)
        ''')
        conexao.commit()
        # A enquete tem as tabelas dela (opções e votos)
        Enquete.criar_tabelas()


    # Transforma linha do banco em objeto Postagem
    @staticmethod
    def _de_linha(linha):
        return Postagem(
            autor_id=linha[1], titulo=linha[3], texto=linha[4], id=linha[0],
            data=linha[5], autor_nome=linha[2], pontos=linha[6], qtd_comentarios=linha[7],
            tem_enquete=linha[8] > 0,
        )


    # Guarda postagem 
    def salvar(self):
        cursor.execute(
            "INSERT INTO postagens (autor_id, titulo, texto) VALUES (?, ?, ?)",
            (self.autor_id, self.titulo, self.texto),
        )
        self.id = cursor.lastrowid  # id da postagem nova (enquete precisa)
        conexao.commit()


    # Lista as postagens em ordem (pontos = mais curtidas ou novas = mais recentes)
    @staticmethod
    def listar(ordem="pontos", limite=10):
        if ordem == "pontos":
            ordenar_por = "(SELECT COALESCE(SUM(valor), 0) FROM votos WHERE postagem_id = p.id) DESC, p.id DESC"
        else:
            ordenar_por = "p.id DESC"
        cursor.execute(f"{Postagem._SELECT} ORDER BY {ordenar_por} LIMIT ?", (limite,))
        return [Postagem._de_linha(linha) for linha in cursor.fetchall()]


    # Procura uma postagem pelo id (devolve None se não existir)
    @staticmethod
    def procurar(id):
        cursor.execute(f"{Postagem._SELECT} WHERE p.id = ?", (id,))
        linha = cursor.fetchone()
        return Postagem._de_linha(linha) if linha else None


    # Apaga a postagem 
    def apagar(self):
        cursor.execute("DELETE FROM postagens WHERE id = ?", (self.id,))
        conexao.commit()


    # Qual foi o voto dessa pessoa? 1 = like, -1 = dislike, 0 = não votou
    def voto_de(self, usuario_id):
        cursor.execute(
            "SELECT valor FROM votos WHERE usuario_id = ? AND postagem_id = ?",
            (usuario_id, self.id),
        )
        linha = cursor.fetchone()
        return linha[0] if linha else 0


    # Vota (votar igual de novo tira o voto, votar diferente troca o voto)
    def votar(self, usuario_id, valor):
        voto_atual = self.voto_de(usuario_id)
        if voto_atual == valor:
            cursor.execute(
                "DELETE FROM votos WHERE usuario_id = ? AND postagem_id = ?",
                (usuario_id, self.id),
            )
        elif voto_atual == 0:
            cursor.execute(
                "INSERT INTO votos (usuario_id, postagem_id, valor) VALUES (?, ?, ?)",
                (usuario_id, self.id, valor),
            )
        else:
            cursor.execute(
                "UPDATE votos SET valor = ? WHERE usuario_id = ? AND postagem_id = ?",
                (valor, usuario_id, self.id),
            )
        conexao.commit()


    # Guarda comentário na postagem
    def comentar(self, autor_id, texto):
        cursor.execute(
            "INSERT INTO comentarios (postagem_id, autor_id, texto) VALUES (?, ?, ?)",
            (self.id, autor_id, texto),
        )
        conexao.commit()


    # Procura comentários
    def procurar_comentarios(self):
        cursor.execute(
            '''SELECT u.nome_usuario, c.texto, c.data
               FROM comentarios c
               JOIN usuarios_ruranimais u ON u.id = c.autor_id
               WHERE c.postagem_id = ?
               ORDER BY c.id''',
            (self.id,),
        )
        return [Comentario(linha[0], linha[1], linha[2]) for linha in cursor.fetchall()]