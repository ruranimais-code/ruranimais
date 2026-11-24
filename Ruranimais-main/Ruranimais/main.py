from pathlib import Path
import sys

# Tava dando problema pra rodar pra mim e tive q adicionar isso </3
raiz_projeto = Path(__file__).resolve().parent
if str(raiz_projeto) not in sys.path:
    sys.path.insert(0, str(raiz_projeto))

# Imports
import time

from playsound3 import playsound

from funcoes.util import Util, amarelo, conexao, cursor, rprint, verde, vermelho
from funcoes.mapa import Mapa
from social.chat import menu_chat
from social.feed import menu_feed
from social.mensagem import Mensagem
from social.postagem import Postagem
from usuario.atualizar import atualizar_dados
from usuario.cadastro import cadastrar_usuario
from usuario.login import login
from usuario.usuario import Usuario

# Musiquinha eba !!
musica_menu = Path(__file__).resolve().parent / "assets" / "musga_menu.mp3"
playsound(str(musica_menu), False)

# Criação do Banco de Dados
cursor.execute(''' CREATE TABLE IF NOT EXISTS usuarios_ruranimais (
               id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               nome_usuario TEXT NOT NULL,
               email TEXT NOT NULL,
               senha TEXT NOT NULL,
               cpf TEXT NOT NULL)
''')
conexao.commit()
Mensagem.criar_tabela()
Postagem.criar_tabelas()

confirmacao_log = []

# Menu Ruranimais :3
def menu_inicial():
    while True:
        Util.limpar_terminal
        rprint(f"\n[{vermelho}]===============================[/{vermelho}]")
        rprint(f":heart:  𖹭  [{verde}][bold]R U R A N I M A I S[/bold][/{verde}] 𖹭 :heart:")
        rprint(f"[{vermelho}]===============================\n[/{vermelho}]")
        rprint(f"[{verde}][bold]Digite o comando destacado ou o número associado para prosseguir.[/bold][/{verde}]")
        rprint(f"1 - [{amarelo}]Cadastrar[/{amarelo}] usuário\n"
               f"2 - [{amarelo}]Login[/{amarelo}] de usuário\n"
               f"3 - [{amarelo}]Perfil[/{amarelo}]\n"
               f"4 - [{amarelo}]Atualizar[/{amarelo}] Dados\n"
               f"5 - [{amarelo}]Conversas[/{amarelo}] (mensagens)\n"
               f"6 - [{amarelo}]Feed[/{amarelo}] de postagens\n"
               f"7 - [{amarelo}]Mapa[/{amarelo}]\n"
               f"8 - [{amarelo}]Sair[/{amarelo}] do programa\n"
               f"\n[{amarelo}][bold]Escolha uma opção: [/bold][/{amarelo}]\n"
               )

        opcao = input("")


        if opcao.lower() == "cadastrar" or opcao == "1":
            Util.limpar_terminal()
            cadastrar_usuario()
            print("Após o cadastro, é necessário realizar o login para acessar o sistema.")


        elif opcao.lower() == "login" or opcao == "2":
            lista_dados_usuario = login()
            if lista_dados_usuario is not None:
                confirmacao_log.append("1")
            else:
                confirmacao_log.clear()


        elif opcao.lower() == "perfil" or opcao == "3":
            if len(confirmacao_log) == 0:
                Util.limpar_terminal()
                print("\nVocê não está logado. Faça o login primeiro.")
                time.sleep(2)
            else:
                ordem_dados = ["ID: ", "Nome: ", "Email: ", "CPF: "]
                dados_visiveis = (
                    lista_dados_usuario[0],
                    lista_dados_usuario[1],
                    lista_dados_usuario[2],
                    lista_dados_usuario[4],
                )
                for a, b in zip(ordem_dados, dados_visiveis):
                    print(a)
                    print(b)

                    
        elif opcao.lower() == "atualizar" or opcao == "4":
            if len(confirmacao_log) == 0:
                Util.limpar_terminal()
                print("\nVocê não está logado. Faça o login primeiro.")
                time.sleep(2)
            else:
                Util.limpar_terminal()
                resultado_atualizacao = atualizar_dados(lista_dados_usuario)
                if resultado_atualizacao is True:
                    confirmacao_log.clear()
                    lista_dados_usuario = None
                elif resultado_atualizacao is not None:
                    lista_dados_usuario = resultado_atualizacao
                else:
                    rprint(f"[{amarelo}]Voltando...[/{amarelo}]")


        elif opcao.lower() == "conversas" or opcao == "5":
            if len(confirmacao_log) == 0:
                Util.limpar_terminal()
                print("\nVocê não está logado. Faça o login primeiro.")
                time.sleep(2)
            else:
                menu_chat(Usuario.from_tupla(lista_dados_usuario))
                Util.limpar_terminal()


        elif opcao.lower() == "feed" or opcao == "6":
            if len(confirmacao_log) == 0:
                Util.limpar_terminal()
                print("\nVocê não está logado. Faça o login primeiro.")
                time.sleep(2)
            else:
                menu_feed(Usuario.from_tupla(lista_dados_usuario))
                Util.limpar_terminal()


        elif opcao.lower() == "mapa" or opcao == "7":
            Util.limpar_terminal()
            Mapa.abrir_mapa()


        elif opcao.lower() == "sair" or opcao == "8":
            Util.limpar_terminal()
            rprint("\n\n\n[#eea103][bold]Até logo![/bold][/#eea103]\n\n\n")
            exit()

        
        else:
            Util.limpar_terminal()
            rprint(
                   f"[{vermelho}]=====================[/{vermelho}]\n\n"
                   f"[bold][{vermelho}]Opção inválida! Tente novamente :)[/{vermelho}][/bold]\n\n"
                   f"[{vermelho}]=====================[/{vermelho}]\n\n"
                  )
            time.sleep(2)
            Util.limpar_terminal()


# Início do programa
Util.mostrar_logo() # Mostra logo do Ruranimais
menu_inicial()