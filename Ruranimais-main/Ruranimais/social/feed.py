# Imports
import time

from rich.markup import escape  # Evita que algo digitado dps vire estilo do rich

from funcoes.util import Util, amarelo, rprint, verde, vermelho
from social.enquete import Enquete
from social.postagem import Postagem


# Menu do feed, lista de postagens
def menu_feed(usuario):
    ordem = "pontos"
    while True:
        Util.limpar_terminal()
        Util.mostrar_titulo("FEED - MAIS CURTIDAS" if ordem == "pontos" else "FEED - MAIS RECENTES")

        postagens = Postagem.listar(ordem)
        if len(postagens) == 0:
            rprint(f"[{amarelo}]Nenhuma postagem ainda. Digite N para criar a primeira![/{amarelo}]")
        for numero, postagem in enumerate(postagens, 1):
            marca_enquete = " 📊" if postagem.tem_enquete else ""
            rprint(f"{numero} - [{verde}][bold]{postagem.pontos}[/bold][/{verde}] pontos | {escape(postagem.titulo)}{marca_enquete}")
            rprint(f"      [dim]por {postagem.autor_nome} · {Util.formatar_data(postagem.data)} · {postagem.qtd_comentarios} comentário(s)[/dim]")

        rprint(
            f"\n[{amarelo}]número do post[/{amarelo}] - Abrir    [{amarelo}]N[/{amarelo}] - Nova postagem    "
            f"[{amarelo}]O[/{amarelo}] - Trocar ordem    [{amarelo}]V[/{amarelo}] - Voltar"
        )
        opcao = input("").strip().lower()

        if opcao == "voltar" or opcao == "v":
            break
        elif opcao == "nova" or opcao == "n":
            criar_postagem(usuario)
        elif opcao == "ordem" or opcao == "o":
            ordem = "novas" if ordem == "pontos" else "pontos"
        elif opcao.isdigit() and 1 <= int(opcao) <= len(postagens):
            ver_postagem(usuario, postagens[int(opcao) - 1].id)
        else:
            rprint(f"\n❌[{vermelho}]Opção inválida[/{vermelho}]")
            time.sleep(1)


# Cria uma postagem nova
def criar_postagem(usuario):
    Util.limpar_terminal()
    Util.mostrar_titulo("NOVA POSTAGEM")

    while True:
        titulo = input("Título (Enter para cancelar): ").strip()
        if titulo == "":
            return
        if len(titulo) < 3 or len(titulo) > 100:
            rprint(f"\n❌[{vermelho}]O título precisa ter entre 3 e 100 caracteres[/{vermelho}]")
            continue
        break

    while True:
        texto = input("Texto (opcional): ").strip()
        if len(texto) > 2000:
            rprint(f"\n❌[{vermelho}]O texto pode ter no máximo 2000 caracteres[/{vermelho}]")
            continue
        break

    # Enquete opcional, título vira pergunta
    opcoes_enquete = []
    if input("Quer adicionar uma enquete? (s/n): ").strip().lower() == "s":
        opcoes_enquete = pedir_opcoes_enquete()

    postagem = Postagem(usuario.id, titulo, texto)
    postagem.salvar()
    if opcoes_enquete:
        Enquete(postagem.id).criar(opcoes_enquete)
    rprint(f"\n[{verde}]Postagem publicada![/{verde}]")
    time.sleep(1)


# Ver post mostra comentários e permite votar/comentar
def ver_postagem(usuario, id_postagem):
    while True:
        # Procura de novo a cada volta pra pontos e comentários ficarem atualizados
        postagem = Postagem.procurar(id_postagem)
        if postagem is None:
            return

        Util.limpar_terminal()
        Util.mostrar_titulo("POSTAGEM")
        rprint(f"[bold]{escape(postagem.titulo)}[/bold]")
        rprint(f"[dim]por {postagem.autor_nome} · {Util.formatar_data(postagem.data)}[/dim]\n")
        if postagem.texto != "":
            rprint(escape(postagem.texto) + "\n")

        meu_voto = postagem.voto_de(usuario.id)
        if meu_voto == 1:
            seta = f"[{verde}]▲[/{verde}]"
        elif meu_voto == -1:
            seta = f"[{vermelho}]▼[/{vermelho}]"
        else:
            seta = "•"
        rprint(f"{seta} [bold]{postagem.pontos}[/bold] pontos")

        # Enquete (só se postagem tiver)
        enquete = Enquete(postagem.id)
        opcoes_enquete = enquete.procurar_opcoes() if postagem.tem_enquete else []
        if opcoes_enquete:
            mostrar_enquete(opcoes_enquete, enquete.voto_de(usuario.id))

        comentarios = postagem.procurar_comentarios()
        rprint(f"\n[{amarelo}]--- Comentários ({len(comentarios)}) ---[/{amarelo}]")
        for comentario in comentarios:
            rprint(f"[bold]{comentario.autor_nome}[/bold] [dim]{Util.formatar_data(comentario.data)}[/dim]")
            rprint(f"  {escape(comentario.texto)}")

        # Só o autor vê a opção de apagar
        opcao_apagar = f"    [{amarelo}]D[/{amarelo}] - Apagar" if postagem.autor_id == usuario.id else ""
        opcao_enquete = f"    [{amarelo}]E[/{amarelo}] - Votar na enquete" if opcoes_enquete else ""
        rprint(
            f"\n[{amarelo}]+[/{amarelo}] like    [{amarelo}]-[/{amarelo}] dislike    "
            f"[{amarelo}]C[/{amarelo}] - Comentar{opcao_enquete}{opcao_apagar}    [{amarelo}]V[/{amarelo}] - Voltar"
        )
        opcao = input("").strip().lower()

        if opcao == "voltar" or opcao == "v":
            return
        elif opcao == "+":
            postagem.votar(usuario.id, 1)
        elif opcao == "-":
            postagem.votar(usuario.id, -1)
        elif opcao == "comentar" or opcao == "c":
            texto = input("Comentário (Enter para cancelar): ").strip()
            if texto == "":
                continue
            if len(texto) > 500:
                rprint(f"\n❌[{vermelho}]Comentário muito grande (máximo 500 caracteres)[/{vermelho}]")
                time.sleep(2)
                continue
            postagem.comentar(usuario.id, texto)
        elif (opcao == "enquete" or opcao == "e") and opcoes_enquete:
            # Votar na mesma opção de novo tira o voto, votar em outra troca o voto
            escolha = input("Número da opção (Enter para cancelar): ").strip()
            if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes_enquete):
                enquete.votar(usuario.id, opcoes_enquete[int(escolha) - 1].id)
            elif escolha != "":
                rprint(f"\n❌[{vermelho}]Opção inválida[/{vermelho}]")
                time.sleep(1)
        elif (opcao == "apagar" or opcao == "d") and postagem.autor_id == usuario.id:
            if input("Apagar essa postagem? (s/n): ").strip().lower() == "s":
                postagem.apagar()
                return


# Pergunta as opções da enquete (devolve lista de textos ou [] se desistir)
def pedir_opcoes_enquete():
    rprint(f"\n[{amarelo}]O título da postagem vai ser a pergunta da enquete.[/{amarelo}]")
    rprint(f"Digite de {Enquete.MINIMO_OPCOES} a {Enquete.MAXIMO_OPCOES} opções. Enter em branco termina (na 1ª opção, cancela a enquete).\n")
    opcoes = []
    while len(opcoes) < Enquete.MAXIMO_OPCOES:
        texto = input(f"Opção {len(opcoes) + 1}: ").strip()
        if texto == "":
            if len(opcoes) == 0:
                return []
            if len(opcoes) < Enquete.MINIMO_OPCOES:
                rprint(f"\n❌[{vermelho}]A enquete precisa de pelo menos {Enquete.MINIMO_OPCOES} opções[/{vermelho}]")
                continue
            break
        opcao_valida, mensagem = Enquete.validar_opcao(texto, opcoes)
        if not opcao_valida:
            rprint(f"\n❌[{vermelho}]{mensagem}[/{vermelho}]")
            continue
        opcoes.append(texto)
    return opcoes


# Mostra as opções da enquete com barrinha de porcentagem
def mostrar_enquete(opcoes, id_meu_voto):
    total = Enquete.total_votos(opcoes)
    rprint(f"\n[{amarelo}]--- Enquete ({total} voto(s)) ---[/{amarelo}]")
    for numero, opcao in enumerate(opcoes, 1):
        percentual = round(opcao.votos * 100 / total) if total > 0 else 0
        cheias = round(percentual / 10)
        barra = "█" * cheias + "░" * (10 - cheias)
        meu_voto = f" [{verde}]◀ seu voto[/{verde}]" if opcao.id == id_meu_voto else ""
        rprint(f"{numero} - {escape(opcao.texto)}")
        rprint(f"      [{verde}]{barra}[/{verde}] {percentual}% ({opcao.votos}){meu_voto}")