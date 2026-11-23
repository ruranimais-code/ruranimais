import os
import re
from datetime import datetime, timedelta
from smtplib import SMTPException

import requests
from dotenv import load_dotenv

from funcoes.enviar_email import EnviarEmail
from funcoes.util import amarelo, cursor, rprint, verde, vermelho


class Validacao:

    # Pra não poder usar dados que já foram cadastrados
    @staticmethod
    def _campo_duplicado(nome_usuario=None, email=None, cpf=None):
        # Vai atrás de ver as informações do usuário
        cursor.execute(
            "SELECT nome_usuario, email, cpf FROM usuarios_ruranimais"
        )
        for nome_cadastrado, email_cadastrado, cpf_cadastrado in cursor.fetchall():
            if nome_usuario is not None and nome_usuario == nome_cadastrado:
                return "Nome de usuário"
            if email is not None and email.casefold() == email_cadastrado.casefold():
                return "E-mail"
            if cpf is not None and Validacao.limpar_cpf(cpf) == Validacao.limpar_cpf(cpf_cadastrado):
                return "CPF"
        return None


    # Confirmar se nome de usuário é válido
    @staticmethod
    def verificar_nome(nome_usuario):
            if len(nome_usuario) > 12:            
                return False, "Nome inválido. Digite um nome com no máximo 12 caracteres"
            elif len(nome_usuario) < 3:
                return False, "Nome inválido. Digite um nome com pelo menos 3 caracteres"
            elif " " in nome_usuario:
                return False, "Nome inválido. O nome não pode conter espaços"
            elif not re.fullmatch(r"[a-zA-Z0-9_]+", nome_usuario):
                return False,"Nome inválido. O nome só pode conter letras, números e underscore/underline"

            # Pra não poder usar dados que já foram cadastrados
            campo_duplicado = Validacao._campo_duplicado(nome_usuario=nome_usuario)
            if campo_duplicado:
                return False, "Usuário já existe"
            else:
                return True, "𖹭"


    # Confirmar se a senha é válida
    @staticmethod
    def verificar_senha(senha):
        if len(senha) < 8:
            return False, "Senha inválida. A senha deve ter pelo menos 8 caracteres"
        elif not re.search(r"[A-Z]", senha):
            return False, "Senha inválida. A senha deve conter pelo menos uma letra maiúscula"
        elif not re.search(r"[a-z]", senha):
            return False, "Senha inválida. A senha deve conter pelo menos uma letra minúscula"
        elif not re.search(r"\d", senha):
            return False, "Senha inválida. A senha deve conter pelo menos um número"
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            return False, "Senha inválida. A senha deve conter pelo menos um caractere especial"
        else:
            return True, "Senha válida"


    # Carrega o que tem dentro do .env
    load_dotenv()
    if not os.environ.get("API_KEY_CPF"):
        raise EnvironmentError(
            "A variável de ambiente API_KEY_CPF não está definida"
        )


    # Tira os caracteres nâo numéricos do cpf
    @staticmethod
    def limpar_cpf(cpf):
        return re.sub(r'\D', '', cpf)


    # Verifica se o cpf tem 11 >números<
    @staticmethod
    def validar_cpf(cpf):
        cpf = Validacao.limpar_cpf(cpf)
        if len(cpf) != 11 or not cpf.isascii() or not cpf.isdigit():
            return False, "CPF deve conter 11 dígitos numéricos"
        # Verifica se todos os digitos são iguais
        if cpf == cpf[0] * 11:
            return False, "Formato inválido"
        else:
            return True, "Formato válido!"


    # Verifica se cpf existe mesmo
    @staticmethod
    def verificar_cpf(cpf):
        cpf_valido, mensagem_cpf = Validacao.validar_cpf(cpf)
        if not cpf_valido:
            return False, mensagem_cpf

        cpf = Validacao.limpar_cpf(cpf)
        url = f"https://api.cpfhub.io/cpf/{cpf}"
        headers = {
            "x-api-key": os.environ.get("API_KEY_CPF"),
            "Accept": "application/json"
        }

        # Vários tratamentos de acordo com resposta da api
        try:
            resposta = requests.get(url, headers=headers, timeout=30)
            if resposta.status_code == 200:
                data = resposta.json()
                if not isinstance(data, dict) or not isinstance(data.get("success"), bool):
                    return False, "API retornou resposta inválida."
                if data["success"]:
                    return True, "CPF válido"
                else:
                    return False, "CPF inválido"
            elif resposta.status_code == 404:
                return False, "CPF não encontrado"
            return False, f"Erro na API: HTTP {resposta.status_code}."
        except requests.exceptions.RequestException as erro:
            return False, f"Erro de conexão: {erro}"
        except ValueError as erro:
            return False, f"API retornou JSON inválido: {erro}"


    # Função pra verificar o codigo do email pra facilitar minha vida
    @staticmethod
    def verificar_codigo_email(email, enviar_email, finalidade):
        codigo = EnviarEmail.gerar_codigo_aleatorio()
        expira = datetime.now() + timedelta(minutes=10)

        rprint(f"\n[{amarelo}]Enviando código para {email}... [/{amarelo}]")
        try:
            enviar_email(email, codigo)
        except (OSError, SMTPException) as erro:
            rprint(f"\n❌[{vermelho}]Falha ao enviar o código[/{vermelho}]")
            print(f"Erro: {erro}")
            return False

        rprint(
            f"\n[{verde}]Código enviado com sucesso!"
            f"Verifique sua caixa de entrada e spam[/{verde}]"
        )
        for tentativa in range(1, 4):
            codigo_digitado = input(
                "Digite o código de verificação enviado para seu email: "
            ).strip().upper()
            if datetime.now() > expira:
                rprint(
                    f"\n❌[{vermelho}]Código expirado"
                    f"Solicite um novo código[/{vermelho}]"
                )
                return False
            if codigo_digitado == codigo:
                rprint(f"\n[{verde}]{finalidade} verificado com sucesso![/{verde}]")
                return True

            rprint(f"\n❌[{vermelho}]Código incorreto\nTentativas restantes: {3 - tentativa}[/{vermelho}]")

        rprint(f"\n❌[{vermelho}]Número máximo de tentativas atingido\nSolicite um novo código[/{vermelho}]")
        return False