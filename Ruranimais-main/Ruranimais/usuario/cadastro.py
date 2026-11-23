# Imports
from funcoes.enviar_email import EnviarEmail
from funcoes.senha import Senha
from funcoes.util import Util, amarelo, conexao, cursor, rprint, verde, vermelho
from funcoes.verificar_dados import Validacao


# Início do cadastro ebaa
def cadastrar_usuario():
    Util.limpar_terminal()
    rprint(f"\n[{vermelho}]===============================[/{vermelho}]")
    rprint(f":heart:  𖹭  [{verde}][bold]CADASTRO DE USUÁRIO[/bold][/{verde}] 𖹭 :heart:")
    rprint(f"[{vermelho}]===============================[/{vermelho}]\n")

    # Nome de usuário + validação
    while True:
        nome_usuario = input("Nome de usuário:").strip()
        nome_valido, mensagem_nome = Validacao.verificar_nome(nome_usuario)
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
            campo_duplicado = Validacao._campo_duplicado(nome_usuario=nome_usuario, email=email,)
            if campo_duplicado:
                rprint(f"\n❌[{vermelho}]{campo_duplicado} já está em uso. Informe outro[/{vermelho}]")
                continue

            if not Validacao.verificar_codigo_email(email, EnviarEmail.enviar_email_cad, "Email"):
                return

            break

    # Inserir cpf + verificar se cpf existe
    while True:
        cpf = input("Cpf: ").strip()
        cpf_valido, mensagem_cpf = Validacao.validar_cpf(cpf)
        if not cpf_valido:
            rprint(f"\n❌[{vermelho}]{mensagem_cpf}[/{vermelho}]")
            continue

        # Pra não poder usar dados que já foram cadastrados
        campo_duplicado = Validacao._campo_duplicado(nome_usuario=nome_usuario, email=email, cpf=cpf,)
        if campo_duplicado:
            rprint(f"\n❌[{vermelho}]{campo_duplicado} já está em uso. Informe outro[/{vermelho}]")
            continue

        rprint(f"\n[{amarelo}]Aguarde um instante...[/{amarelo}]")

        ok, resultado = Validacao.verificar_cpf(cpf)

        if ok:
            rprint(f"\n[{verde}]CPF verificado com sucesso")
            break
        else:
            rprint(f"\n❌[{vermelho}]{resultado}[/{vermelho}]")

    # Criar senha + confirmar senha + validar senha
    while True:
        rprint (f"\nSenha precisa conter:\n- Pelo menos 8 caracteres\n- Uma letra maiúscula\n- Uma letra minúscula\n- Um número\n- Um caractere especial")
        senha = input("Senha: ").strip()
        senha_valida, mensagem_senha = Validacao.verificar_senha(senha)
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
    campo_duplicado = Validacao._campo_duplicado(nome_usuario=nome_usuario, email=email, cpf=cpf,)
    if campo_duplicado:
        conexao.rollback()
        rprint(f"\n❌[{vermelho}]{campo_duplicado} já cadastrado. Cadastro cancelado[/{vermelho}]")
        return

    cursor.execute(
        '''INSERT INTO usuarios_ruranimais (nome_usuario, email, senha, cpf)
           VALUES (?, ?, ?, ?)''',
        (nome_usuario, email, Senha.gerar_hash(senha), cpf),  # Guarda o hash eba
    )
    # Comita as informações no banco de dados
    conexao.commit()

    rprint(f"\n[{verde}]Usuário cadastrado com sucesso![/{verde}]")