# Imports
from funcoes.util import conexao, cursor

# Mensagem 
class Mensagem:
    def __init__(self, remetente_id, destinatario_id, texto, id=None, data=None, lida=0):
        self.id = id
        self.remetente_id = remetente_id
        self.destinatario_id = destinatario_id
        self.texto = texto
        self.data = data
        self.lida = lida  # 0 = não lida, 1 = lida


    # Cria a tabela no banco se ainda não existir
    @staticmethod
    def criar_tabela():
        cursor.execute(''' CREATE TABLE IF NOT EXISTS mensagens (
                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       remetente_id INTEGER NOT NULL,
                       destinatario_id INTEGER NOT NULL,
                       texto TEXT NOT NULL,
                       data TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                       lida INTEGER NOT NULL DEFAULT 0,
                       FOREIGN KEY (remetente_id) REFERENCES usuarios_ruranimais(id) ON DELETE CASCADE,
                       FOREIGN KEY (destinatario_id) REFERENCES usuarios_ruranimais(id) ON DELETE CASCADE)
        ''')
        conexao.commit()


    # Guarda a mensagem no banco
    def salvar(self):
        cursor.execute(
            "INSERT INTO mensagens (remetente_id, destinatario_id, texto) VALUES (?, ?, ?)",
            (self.remetente_id, self.destinatario_id, self.texto),
        )
        conexao.commit()


    # Procura todas as mensagens entre duas pessoas da mais antiga pra mais nova
    @staticmethod
    def procurar_conversa(id_a, id_b):
        cursor.execute(
            '''SELECT id, remetente_id, destinatario_id, texto, data, lida
               FROM mensagens
               WHERE (remetente_id = ? AND destinatario_id = ?)
                  OR (remetente_id = ? AND destinatario_id = ?)
               ORDER BY id''',
            (id_a, id_b, id_b, id_a),
        )
        return [
            Mensagem(linha[1], linha[2], linha[3], linha[0], linha[4], linha[5])
            for linha in cursor.fetchall()
        ]
    

    # Marca como lidas as mensagens que passaram por id_leitor
    @staticmethod
    def marcar_como_lidas(id_leitor, id_outro):
        cursor.execute(
            "UPDATE mensagens SET lida = 1 WHERE destinatario_id = ? AND remetente_id = ?",
            (id_leitor, id_outro),
        )
        conexao.commit()


    # Conta mensagens não lidas 
    @staticmethod
    def contar_nao_lidas(id_usuario, id_remetente=None):
        if id_remetente is None:
            cursor.execute(
                "SELECT COUNT(*) FROM mensagens WHERE destinatario_id = ? AND lida = 0",
                (id_usuario,),
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM mensagens WHERE destinatario_id = ? AND remetente_id = ? AND lida = 0",
                (id_usuario, id_remetente),
            )
        return cursor.fetchone()[0]


    # Lista ids que o usuário já conversou 
    @staticmethod
    def listar_contatos(id_usuario):
        cursor.execute(
            '''SELECT remetente_id, destinatario_id FROM mensagens
               WHERE remetente_id = ? OR destinatario_id = ?
               ORDER BY id DESC''',
            (id_usuario, id_usuario),
        )
        contatos = []
        for remetente, destinatario in cursor.fetchall():
            # Outro = não o próprio usuário
            outro = destinatario if remetente == id_usuario else remetente
            if outro not in contatos:
                contatos.append(outro)
        return contatos