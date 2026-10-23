# Bibliotecas
import sqlite3
conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()
from rich import print as rprint
# Imports
import re
from funcoes.verificacao_email import *
from funcoes.crud_funcoes import *
from funcoes.crud_funcoes import _campo_duplicado

# Cores Utilizadas Frequentemente
amarelo = "#EEA103"
vermelho = "#D74013"
azul = "#2B283B"
verde = "#719029"
bege = "#F8E8CF"


# Início do cadastro ebaa
def cadastrar_usuario():
    rprint(f"\n[{vermelho}]===============================[/{vermelho}]")
    rprint(f":heart:  𖹭  [{verde}][bold]CADASTRO DE USUÁRIO[/bold][/{verde}] 𖹭 :heart:")
    rprint(f"[{vermelho}]===============================[/{vermelho}]\n")

    # Nome de usuário + validação
    while True:
        nome_usuario = input("Nome de usuário:").strip()
        nome_valido, mensagem_nome = verificar_nome(nome_usuario)
        if not nome_valido:
            rprint(f"\n❌[{vermelho}]{mensagem_nome}[/{vermelho}]")
            continue
        rprint(f"\n[{verde}]Nome de usuário disponível![/{verde}]")
        break

    # Inserir email + verificação de duas etapas (envio de código e verificação do mesmo)
    while True:
        email = input("E-mail: ").strip()
        if "@" not in email or "." not in email:
            rprint(f"\n❌[{vermelho}]E-mail inválido. Email não contém @ ou endereço válido[/{vermelho}]")
            continue
        elif email.endswith ("@ufrpe.br") == False:
            rprint(f"\n❌[{vermelho}]E-mail inválido. Digite um e-mail institucional da UFRPE[/{vermelho}]")
            continue
        else:

            # Pra não poder usar dados que já foram cadastrados
            campo_duplicado = _campo_duplicado(nome_usuario=nome_usuario, email=email,)
            if campo_duplicado:
                rprint(f"\n❌[{vermelho}]{campo_duplicado} já está em uso. Informe outro[/{vermelho}]")
                continue

            if not verificar_codigo_email(email, enviar_email_con, "Email"):
                return

            break

    # Inserir cpf + verificar se cpf existe
    while True:
        cpf = input("Cpf: ").strip()
        cpf_valido, mensagem_cpf = validar_cpf(cpf)
        if not cpf_valido:
            rprint(f"\n❌[{vermelho}]{mensagem_cpf}[/{vermelho}]")
            continue

        # Pra não poder usar dados que já foram cadastrados
        campo_duplicado = _campo_duplicado(nome_usuario=nome_usuario, email=email, cpf=cpf,)
        if campo_duplicado:
            rprint(f"\n❌[{vermelho}]{campo_duplicado} já está em uso. Informe outro[/{vermelho}]")
            continue

        rprint(f"\n[{amarelo}]Aguarde um instante...[/{amarelo}]")

        ok, resultado = verificar_cpf(cpf)

        if ok:
            rprint(f"\n[{verde}]CPF verificado com sucesso")
            break
        else:
            rprint(f"\n❌[{vermelho}]{resultado}[/{vermelho}]")

    # Criar senha + confirmar senha + validar senha
    while True:
        rprint (f"\nSenha precisa conter:\n- Pelo menos 8 caracteres\n- Uma letra maiúscula\n- Uma letra minúscula\n- Um número\n- Um caractere especial")
        senha = input("Senha: ").strip()
        senha_valida, mensagem_senha = verificar_senha(senha)
        if not senha_valida:
            rprint(f"\n❌[{vermelho}]{mensagem_senha}[/{vermelho}]")
            continue
        confirmacao_senha = input("Confirme sua senha:").strip()
        while confirmacao_senha != senha:
            rprint(f"\n❌[{vermelho}]As senhas não coincidem[/{vermelho}]")
            confirmacao_senha = input("Por favor, tente novamente: ")
        rprint(f"\n[{verde}]Senha criada com sucesso![/{verde}]")
        break

    # Pra não poder usar dados que já foram cadastrados
    conexao.execute("BEGIN IMMEDIATE")
    campo_duplicado = _campo_duplicado(nome_usuario=nome_usuario, email=email, cpf=cpf,)
    if campo_duplicado:
        conexao.rollback()
        rprint(f"\n❌[{vermelho}]{campo_duplicado} já cadastrado. Cadastro cancelado[/{vermelho}]")
        return

    cursor.execute(
        '''INSERT INTO usuarios_ruranimais (nome_usuario, email, senha, cpf)
           VALUES (?, ?, ?, ?)''',
        (nome_usuario, email, senha, cpf),
    )
    # Comita informações no banco de dados
    conexao.commit()

    rprint(f"\n[{verde}]Usuário cadastrado com sucesso![/{verde}]")

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
            if senha == dados_usuario[3]:
                if verificar_codigo_email(email, enviar_email_log, "Login"):
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
        dados_usuario = recuperar_senha(dados_usuario)
        if dados_usuario is not None:
            rprint(f"\n[{verde}]Login realizado com sucesso![/{verde}]\nBem vindo novamente ᨐฅ")
        return dados_usuario

# Menu de atualizar dados que legal
def atualizar_dados(dados_usuario):
    while True:
        rprint(f"\n[{vermelho}]===========================[/{vermelho}]")
        rprint(f":heart:  𖹭  [{verde}][bold]ATUALIZAR DADOS[/bold][/{verde}] 𖹭 :heart:")
        rprint(f"[{vermelho}]===========================\n[/{vermelho}]")
        rprint(f"[{verde}][bold]Digite o comando destacado ou o número associado para prosseguir.[/bold][/{verde}]")
        rprint(f"1 - Atualizar [{amarelo}]nome[/{amarelo}]")
        rprint(f"2 - Atualizar [{amarelo}]senha[/{amarelo}]")
        rprint(f"3 - [{amarelo}]Deletar[/{amarelo}] conta")
        rprint(f"4 - [{amarelo}]Voltar[/{amarelo}] pro menu\n")
        
        opcao = input("")

        # Chama função que troca o nome de usuário
        if opcao.lower() == "nome" or opcao == "1":      
            nome_usuario_anterior = dados_usuario[1]      
            dados_usuario = atualizar_nome_usuario(dados_usuario)
            if dados_usuario[1] != nome_usuario_anterior:
                rprint(f"\n[{verde}]Nome de usuário atualizado com sucesso![/{verde}]")
                return dados_usuario

        # Chama função que atualiza senha
        elif opcao.lower() == "senha" or opcao == "2":
            dados_usuario = atualizar_senha(dados_usuario)
            if dados_usuario is not None:
                rprint(f"\n[{verde}]Senha atualizada com sucesso![/{verde}]")
                return dados_usuario

        # Função deletar conta + conta deletada
        elif opcao.lower() == "deletar" or opcao == "3":
            conta_deletada = deletar_usuario(
                dados_usuario[2],
                dados_usuario[1],
                dados_usuario[4],
                dados_usuario[3],
            )
            if conta_deletada:
                return True
            if conta_deletada is False:
                continue
            rprint(f"\n❌[{vermelho}]Não foi possível deletar a conta[/{vermelho}]")

        # Volta pro menu
        elif opcao.lower() == "voltar" or opcao == "4":
            break

        # Msg de erro
        else:
            rprint(f"\n❌[{vermelho}]Por favor escolha uma opção válida[/{vermelho}]")