# Imports
from funcoes.atualizar_dados import Atualizacao
from funcoes.util import amarelo, rprint, verde, vermelho


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
            dados_usuario = Atualizacao.atualizar_nome_usuario(dados_usuario)
            if dados_usuario[1] != nome_usuario_anterior:
                rprint(f"\n[{verde}]Nome de usuário atualizado com sucesso![/{verde}]")
                return dados_usuario

        # Chama função que atualiza senha
        elif opcao.lower() == "senha" or opcao == "2":
            dados_usuario = Atualizacao.atualizar_senha(dados_usuario)
            if dados_usuario is not None:
                rprint(f"\n[{verde}]Senha atualizada com sucesso![/{verde}]")
                return dados_usuario

        # Função deletar conta + conta deletada
        elif opcao.lower() == "deletar" or opcao == "3":
            conta_deletada = Atualizacao.deletar_usuario(
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