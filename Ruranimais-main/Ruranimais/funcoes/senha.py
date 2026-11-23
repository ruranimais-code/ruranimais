# Imports
import hashlib
import hmac
import secrets


# Guarda o hash ao invés do texto das senhas
class Senha:
    PREFIXO = "pbkdf2"
    ITERACOES = 600_000  # Quantas vezes embaralha O.o

    # Tá cm esse nome pq é como me foi explicado </3
    # Mas sal é um pedaço aleatório pra duas pessoas cm msm senha terem hash diferentes
    @staticmethod
    def gerar_hash(senha):
        sal = secrets.token_bytes(16)
        hash_calculado = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, Senha.ITERACOES)
        return f"{Senha.PREFIXO}${Senha.ITERACOES}${sal.hex()}${hash_calculado.hex()}"

    # True se oq ta guardado no banco já é um hash (False = conta criada antes)
    @staticmethod
    def eh_hash(guardado):
        return guardado.startswith(f"{Senha.PREFIXO}$")

    # Confere a senha digitada com o que está no banco
    # No caso pega o pedaço e compara
    @staticmethod
    def verificar(senha_digitada, guardado):
        if not Senha.eh_hash(guardado):
            # Conta antiga: a senha ainda está em texto puro, compara direto
            return hmac.compare_digest(senha_digitada.encode("utf-8"), guardado.encode("utf-8"))
        _, iteracoes, sal_hex, hash_hex = guardado.split("$")
        hash_novo = hashlib.pbkdf2_hmac(
            "sha256", senha_digitada.encode("utf-8"), bytes.fromhex(sal_hex), int(iteracoes)
        )
        return hmac.compare_digest(hash_novo, bytes.fromhex(hash_hex))