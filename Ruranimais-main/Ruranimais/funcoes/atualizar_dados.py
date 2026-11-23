# Imports
import time

from funcoes.enviar_email import EnviarEmail
from funcoes.senha import Senha
from funcoes.util import amarelo, conexao, cursor, rprint, verde, vermelho
from funcoes.verificar_dados import Validacao


class Atualizacao:

    # Cria nova senha
    @staticmethod
    def recuperar_senha(dados_usuario):
        cpf_digitado = input("Digite seu CPF para confirmar sua identidade: ").strip()
        if Validacao.limpar_cpf(cpf_digitado) != Validacao.limpar_cpf(dados_usuario[4]):
            rprint(f"\n❌[{vermelho}]CPF incorreto[/{vermelho}]\nVoltando para o menu...")
            time.sleep(2)
            return None

        if not Validacao.verificar_codigo_email(dados_usuario[2], EnviarEmail.enviar_email_senha, "Recuperação de senha"):
            return None

        while True:
            rprint (f"\nSenha precisa conter:\n- Pelo menos 8 caracteres\n- Uma letra maiúscula\n- Uma letra minúscula\n- Um número\n- Um caractere especial")
            nova_senha = input("Digite sua nova senha: ").strip()
            senha_valida, mensagem = Validacao.verificar_senha(nova_senha)
            if not senha_valida:
                rprint(f"\n❌[{vermelho}]{mensagem}[/{vermelho}]")
                continue

            confirmacao = input("Confirme sua nova senha: ").strip()
            if confirmacao != nova_senha:
                rprint(f"\n❌[{vermelho}]As senhas não coincidem[/{vermelho}]")
                continue
            break

        # Vai atrás da senha no banco de dados pra atualizar
        cursor.execute(
            "UPDATE usuarios_ruranimais SET senha = ? WHERE id = ?",
            (Senha.gerar_hash(nova_senha), dados_usuario[0]),
        )
        conexao.commit()
        rprint(f"\n[{verde}]Senha redefinida com sucesso![/{verde}]")
        cursor.execute(
            "SELECT * FROM usuarios_ruranimais WHERE id = ?",
            (dados_usuario[0],),
        )
        return cursor.fetchone()


    # Deletar conta
    @staticmethod
    def deletar_usuario(email, nome_usuario, cpf, senha):
        while True:
            rprint(f"\n[{vermelho}]Deseja deletar sua conta?[/{vermelho}]")
            deseja_deletar = input(
                f"OBS.: Essa ação não pode ser desfeita!\n(s/n): "
            ).strip().lower()
            if deseja_deletar == "s":
                break
            if deseja_deletar == "n":
                rprint(f"[{verde}]Ebaaa, sua conta continua intacta![/{verde}]")
                return False
            rprint(f"[{vermelho}]Opção inválida. Digite s ou n.[/{vermelho}]")

        # Pede informações usadas no login pra confirmar que usuário quer deletar conta
        email_digitado = input("Informe seu email para confirmar: ").strip()
        senha_digitada = input("Informe sua senha para confirmar: ").strip()
        # N tem mais senha_verificar aqui por conta do hash
        if email_digitado != email or not Senha.verificar(senha_digitada, senha):
            rprint(f"\n❌[{vermelho}]Email e/ou senha incorretos[/{vermelho}]\n\nNão foi possível deletar conta.")
            time.sleep(1)
            return None
        
    # Vai atrás de deletar as informações do usuário
        cursor.execute(
            """SELECT id FROM usuarios_ruranimais
            WHERE email = ? AND nome_usuario = ? AND cpf = ? AND senha = ?""",
            (email, nome_usuario, cpf, senha),
        )
        usuario = cursor.fetchone()
        if usuario is None:
            rprint(f"\n❌[{vermelho}]Não foi possível encontrar a conta[/{vermelho}]")
            return None

        cursor.execute(
            "DELETE FROM usuarios_ruranimais WHERE id = ?",
            (usuario[0],),
        )
        conexao.commit()
        rprint("\nConta deletada com sucesso...\nFoi um prazer ter você conosco!")
        time.sleep (2)
        return True


    # Atualizar senha
    @staticmethod
    def atualizar_senha(dados_usuario):
        while True:
            rprint("\nSenha precisa conter:\n- Pelo menos 8 caracteres\n- Uma letra maiúscula\n- Uma letra minúscula\n- Um número\n- Um caractere especial")
            nova_senha = input("Digite sua nova senha: ").strip()
            senha_valida, mensagem = Validacao.verificar_senha(nova_senha)
            if not senha_valida:
                rprint(f"\n❌[{vermelho}]{mensagem}[/{vermelho}]")
                continue

            confirmacao = input("Confirme sua nova senha: ").strip()
            if confirmacao != nova_senha:
                rprint(f"\n❌[{vermelho}]As senhas não coincidem[/{vermelho}]")
                continue
            break

        # Vai atrás da senha no banco de dados pra atualizar
        cursor.execute(
            "UPDATE usuarios_ruranimais SET senha = ? WHERE id = ?",
            (Senha.gerar_hash(nova_senha), dados_usuario[0]),
        )
        conexao.commit()
        cursor.execute(
            "SELECT * FROM usuarios_ruranimais WHERE id = ?",
            (dados_usuario[0],),
        )
        dados_atualizados = cursor.fetchone()
        if dados_atualizados is None:
            raise LookupError(f"[{vermelho}]Usuário não encontrado :( atualização da senha falha[/{vermelho}]")
        return dados_atualizados


    # Atualizar nome
    @staticmethod
    def atualizar_nome_usuario(dados_usuario):
        while True:
            novo_nome_usuario = input("Nome de usuário:").strip()
            if novo_nome_usuario == dados_usuario[1]:
                rprint(f"\n[{amarelo}]Nome de usuário permanece o mesmo[/{amarelo}]")
                return dados_usuario
            nome_valido, mensagem_nome = Validacao.verificar_nome(novo_nome_usuario)
            if not nome_valido:
                rprint(f"\n❌[{vermelho}]{mensagem_nome}[/{vermelho}]")
                continue
            break

        # Vai atrás de nome_usuario no banco de dados pra atualizar
        cursor.execute(
            "UPDATE usuarios_ruranimais SET nome_usuario = ? WHERE id = ?",
            (novo_nome_usuario, dados_usuario[0]),
            )
        conexao.commit()
        cursor.execute(
            "SELECT * FROM usuarios_ruranimais WHERE id = ?",
            (dados_usuario[0],),
            )
        dados_atualizados = cursor.fetchone()
        if dados_atualizados is None:
            raise LookupError(f"[{vermelho}]Usuário não encontrado :( atualização de nome de usuário falha[/{vermelho}]")
        return dados_atualizados


    # Guarda como hash e devolve dados atualizados de qm fez cadastro antes do hash ser implementado
    @staticmethod
    def converter_senha_para_hash(dados_usuario, senha_digitada):
        if Senha.eh_hash(dados_usuario[3]):
            return dados_usuario
        cursor.execute(
            "UPDATE usuarios_ruranimais SET senha = ? WHERE id = ?",
            (Senha.gerar_hash(senha_digitada), dados_usuario[0]),
        )
        conexao.commit()
        cursor.execute(
            "SELECT * FROM usuarios_ruranimais WHERE id = ?",
            (dados_usuario[0],),
        )
        return cursor.fetchone()