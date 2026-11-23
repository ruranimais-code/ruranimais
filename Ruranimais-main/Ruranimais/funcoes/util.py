# Imports
import datetime
import platform
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

from rich import print as rprint
from rich.console import Console

# Pra acentos e emojis aparecer certinho no terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
console = Console()

# Banco de dados (o banco.db fica na pasta acima do projeto)
raiz_projeto = Path(__file__).resolve().parent.parent
raiz_workspace = raiz_projeto.parent
caminho_banco = raiz_workspace / "banco.db"
conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

# Liga as chaves estrangeiras (sem isso o SQLite n apaga coisa de conta deletada:c)
conexao.execute("PRAGMA foreign_keys = ON")

class Util:

    # Mostra logo da ruranimais
    @staticmethod
    def mostrar_logo(caminho_logo=None):
        arquivo_logo = (
            Path(caminho_logo)
            if caminho_logo is not None
            else Path(__file__).resolve().parent.parent / "assets" / "ruranimaislogo.txt"
        )
        with arquivo_logo.open("r", encoding="utf-8") as f:
            logo= f.read()
        rprint(logo)
        time.sleep(4)
        Util.limpar_terminal()


    # Identificação de Sistema + Limpeza Inicial do Terminal
    @staticmethod
    def limpar_terminal():
        if platform.system() in ("Linux", "Darwin"):
            subprocess.run("clear", shell=True, check=False)
        elif platform.system() == "Windows":
            subprocess.run("cls", shell=True, check=False)


    # Título bonitinho para os menus novos
    @staticmethod
    def mostrar_titulo(titulo):
        barra = "=" * (len(titulo) + 12)
        rprint(f"\n[{vermelho}]{barra}[/{vermelho}]")
        rprint(f":heart:  𖹭  [{verde}][bold]{titulo}[/bold][/{verde}] 𖹭 :heart:")
        rprint(f"[{vermelho}]{barra}[/{vermelho}]\n")


    # Transforma ano-mês-dia hora:minuto:segundo em dia/mês hora:minuto
    @staticmethod
    def formatar_data(data):
        return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S").strftime("%d/%m %H:%M")


# Cores Utilizadas Frequentemente
amarelo = "#EEA103"
vermelho = "#D74013"
azul = "#2B283B"
verde = "#719029"
bege = "#F8E8CF"