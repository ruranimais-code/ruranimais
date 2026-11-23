# Imports
from funcoes.atualizar_dados import Atualizacao
from funcoes.enviar_email import EnviarEmail
from funcoes.util import cursor, rprint, verde, vermelho
from funcoes.verificar_dados import Validacao
from funcoes.senha import Senha


# Login ebaaaaaaa
def login():
    rprint(f"\n[{vermelho}]=============================[/{vermelho}]")
    rprint(f" :heart:  𖹭  [{verde}][bold]LOGIN DE USUÁRIO[/bold][/{verde}] 𖹭 :heart:")
    rprint(f"[{vermelho}]=============================[/{vermelho}]\n")

# Procura email no banco de dados cm alguns requisitos pra ir buscar
    while True:
        email = input("Digite seu email: ").strip()
        if "@" not in email or "." not in email:
            rprint(f"\n❌[{vermelho}]E-mail inválido. Email não contém @ ou endereço válido[/{vermelho}]")
            continue
        elif email.endswith ("@ufrpe.br") == False:
                rprint(f"\n❌[{vermelho}]E-mail inválido. Digite um e-mail institucional da UFRPE[/{vermelho}]")
                continue
        elif cursor.execute(
                "SELECT * FROM usuarios_ruranimais WHERE email = ?",
                (email,),
            ):
            dados_usuario = cursor.fetchone()
            if dados_usuario is None:
                rprint(f"\n❌[{vermelho}]Email não cadastrado![/{vermelho}]")
                continue
        else:
            break

        # Dá 3 chances de acertar a senha
        tentativas_restantes = 3
        while tentativas_restantes > 0:
            senha = input("Digite sua senha: ").strip()
            if Senha.verificar(senha, dados_usuario[3]):
                # Guarda como hash e devolve dados atualizados de qm fez cadastro antes do hash ser implementado
                dados_usuario = Atualizacao.converter_senha_para_hash(dados_usuario, senha)
                if Validacao.verificar_codigo_email(email, EnviarEmail.enviar_email_log, "Login"):
                    return dados_usuario
                return None

            tentativas_restantes -= 1
            rprint(f"\n❌[{vermelho}]Senha incorreta\nTentativas restantes: {tentativas_restantes}[/{vermelho}]")

        # Depois de errar 3 vezes, pergunta se quer redefinir senha
        # Caso não, aplicação é encerrada e usuário volta pro menu
        deseja_recuperar = input("Deseja redefinir sua senha? (s/n): ").strip().lower()
        if deseja_recuperar != "s":
            print (f"Até a próxima :(")
            return None

        # Login realizado se função recuperar_senha prosseguir
        dados_usuario = Atualizacao.recuperar_senha(dados_usuario)
        if dados_usuario is not None:
            rprint(f"\n[{verde}]Login realizado com sucesso![/{verde}]\nBem vindo novamente ᨐฅ")
        return dados_usuario