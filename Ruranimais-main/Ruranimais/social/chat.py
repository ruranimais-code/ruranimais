# Imports
import time

from rich.markup import escape  # Evita que algo digitado dps vire estilo do rich

from funcoes.util import Util, amarelo, rprint, verde, vermelho
from social.mensagem import Mensagem
from usuario.usuario import Usuario


# Menu do chat, lista de conversas
def menu_chat(usuario):
    while True:
        Util.limpar_terminal()
        Util.mostrar_titulo("CONVERSAS")

        contatos = []
        # Procura id dos contatos + ignora usuários deletados
        for id_contato in Mensagem.listar_contatos(usuario.id):
            contato = Usuario.procurar_id(id_contato)
            if contato is not None:
                contatos.append(contato)

        if len(contatos) == 0:
            rprint(f"[{amarelo}]Você ainda não tem conversas. Digite N para começar uma![/{amarelo}]")
        for numero, contato in enumerate(contatos, 1):
            novas = Mensagem.contar_nao_lidas(usuario.id, contato.id)
            aviso = f" [{vermelho}]({novas} nova(s))[/{vermelho}]" if novas > 0 else ""
            rprint(f"{numero} - {contato.nome_usuario}{aviso}")

        rprint(f"\n[{amarelo}]N[/{amarelo}] - Nova conversa    [{amarelo}]V[/{amarelo}] - Voltar")
        opcao = input("").strip().lower()

        if opcao == "voltar" or opcao == "v":
            break
        elif opcao == "nova" or opcao == "n":
            nova_conversa(usuario)
        elif opcao.isdigit() and 1 <= int(opcao) <= len(contatos):
            outro = contatos[int(opcao) - 1]
            conversar(usuario, outro)
        else:
            rprint(f"\n❌[{vermelho}]Opção inválida[/{vermelho}]")
            time.sleep(1)


# Pergunta com quem a pessoa quer falar e abre a conversa
def nova_conversa(usuario):
    nome = input("Quem? (nome de usuário, Enter para cancelar): ").strip()
    if nome == "":
        return
    outro = Usuario.procurar_nome_usuario(nome)
    if outro is None:
        rprint(f"\n❌[{vermelho}]Usuário não encontrado[/{vermelho}]")
        time.sleep(2)
    elif outro.id == usuario.id:
        rprint(f"\n❌[{vermelho}]Você não pode mandar mensagem pra você mesmo[/{vermelho}]")
        time.sleep(2)
    else:
        conversar(usuario, outro)


# Tela da conversa
def conversar(usuario, outro):
    while True:
        Util.limpar_terminal()
        Util.mostrar_titulo(f"CONVERSA COM {outro.nome_usuario.upper()}")

        # Conversa aberta = msg lida
        Mensagem.marcar_como_lidas(usuario.id, outro.id)

        # Mostra só as 30 últimas mensagens
        for mensagem in Mensagem.procurar_conversa(usuario.id, outro.id)[-30:]:
            hora = Util.formatar_data(mensagem.data)
            if mensagem.remetente_id == usuario.id:
                rprint(f"[{verde}]Você:[/{verde}] {escape(mensagem.texto)} [dim]{hora}[/dim]")
            else:
                rprint(f"[{amarelo}]{outro.nome_usuario}:[/{amarelo}] {escape(mensagem.texto)} [dim]{hora}[/dim]")

        # Apertar Enter sem digitar nada atualiza a tela
        texto = input("\nMensagem (Enter para atualizar conversa | digite /sair para sair) ").strip()
        if texto.lower() == "/sair":
            break
        if texto == "":
            continue
        if len(texto) > 500:
            rprint(f"\n❌[{vermelho}]Mensagem muito grande (máximo 500 caracteres)[/{vermelho}]")
            time.sleep(2)
            continue

        Mensagem(usuario.id, outro.id, texto).salvar()