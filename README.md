# 🐾 Ruranimais — A rede social de quem cuida

<p align="center">
  <img width="300" alt="ruranimais_logo" src="https://github.com/user-attachments/assets/f5654f59-383e-4410-aceb-8e0c741977cf">
</p>

O **Ruranimais** é uma rede social em **terminal** criada para a comunidade da **UFRPE**, com foco no cuidado e no monitoramento dos animais que vivem no campus e nos arredores.

---

## 📌 Sobre o Projeto

Apesar de existirem iniciativas que buscam alimentar e ajudar os animais que residem na **UFRPE**, diversos bichinhos, como gatos e cachorros, ainda andam pelo campus recém-machucados.

Por esse e outros motivos, acreditamos que uma rede social focada no monitoramento dos animais, usada pela comunidade discente, pode ajudar a preservar a saúde animal na universidade e, consequentemente, prevenir **zoonoses e acidentes**.

A ferramenta conecta pessoas por toda a região da UFRPE e proximidades, por meio de **Bate-papo, Postagens, Enquetes e Mapeamento**. Essas funcionalidades foram (e continuam sendo) adicionadas gradualmente, release a release.

---

## Releases

### Release 1.0

* Menu principal
* Cadastro de usuário
* Login
* Verificação de duas etapas
* Verificação de CPF
* Perfil, atualização de dados, recuperação de senha e exclusão de conta

### Release 2.0

* Conversas diretas entre usuários
* Criar postagens
* Comentários
* Enquetes
* Hash
* Mapa (folium) com a frequência de encontrar animais no campus
* Código agora em OOP

---

## 🔎 Funcionalidades

| Área | O que o app faz |
| ---- | --------------- |
| 👤 **Conta** | Cadastro, login, perfil, atualização de nome e senha, recuperação de senha e exclusão de conta |
| 🔐 **Segurança** | Verificação em duas etapas por e-mail, verificação de CPF, senhas com hash, requisitos de senha forte |
| 💬 **Bate-papo** | Mensagens diretas, lista de conversas, contador de mensagens não lidas |
| 📝 **Postagens** | Feed, curtidas, comentários e ordenação |
| 📊 **Enquetes** | Enquetes dentro das postagens, com votação e porcentagens |
| 🗺️ **Mapa** | Mapa de calor da frequência de animais no campus |

### Regras de uso

* **Nome de usuário:** de 3 a 12 caracteres, apenas letras, números e "_"
* **Senha:** mínimo de 8 caracteres, com letra maiúscula, minúscula, número e caractere especial
* **Mensagens:** até 500 caracteres
* **Postagens:** título de 3 a 100 caracteres e texto de até 2000
* **Comentários:** até 500 caracteres
* **Enquetes:** de 2 a 6 opções, com até 50 caracteres cada

---

## 🛠️ Tecnologias

O projeto é desenvolvido em **Python**, com interface no terminal e banco de dados **SQLite**.

| Biblioteca | Para que serve |
| ---------- | -------------- |
| `rich` | Cores, formatação e interface do terminal |
| `requests` | Consulta de CPF na API |
| `python-dotenv` | Leitura das variáveis secretas do arquivo .env
| `playsound3` | Música do menu |
| `numpy` | Leitura e tratamento dos dados de frequência |
| `folium` | Mapa de calor |
| `sqlite3`, `smtplib`, `hashlib` | Banco de dados, envio de e-mails e hash de senhas |

---

## 📁 Estrutura do Projeto

```text
(Ruranimais-main)
├── banco.db
└── Ruranimais/
    ├── main.py
    │
    ├── assets/
    │   ├── frequencia_bichinhos.csv
    │   ├── musga_menu.mp3
    │   ├── ruranimaislogo.txt
    │   └── ufrpe.geojson
    │
    ├── funcoes/
    │   ├── .env                       (NÃO vai pro git)
    │   ├── .gitignore
    │   ├── atualizar_dados.py
    │   ├── enviar_email.py
    │   ├── footprint.html
    │   ├── mapa.py
    │   ├── senha.py
    │   ├── util.py
    │   └── verificar_dados.py
    │
    ├── social/
    │   ├── chat.py
    │   ├── enquete.py
    │   ├── feed.py
    │   ├── mensagem.py
    │   └── postagem.py
    └── usuario/
        ├── atualizar.py
        ├── cadastro.py
        ├── login.py
        └── usuario.py
```

---

## 🗄️ Banco de Dados

O banco `banco.db` (SQLite) é criado automaticamente, na pasta acima de `Ruranimais/`, com as tabelas:

| Tabela | Guarda |
| ------ | ------ |
| `usuarios_ruranimais` | Contas dos usuários (com senha em hash) |
| `mensagens` | Mensagens do bate-papo |
| `postagens` | Postagens do feed |
| `comentarios` | Comentários das postagens |
| `votos` | Curtidas e descurtidas |
| `opcoes_enquete` | Opções das enquetes |
| `votos_enquete` | Votos das enquetes |

---

## 🧭 Como Usar

Ao abrir o programa, o menu principal oferece:

| Opção | O que faz |
| ----- | --------- |
| `1` Cadastrar | Cria uma conta (e-mail `@ufrpe.br`, CPF e verificação por código) |
| `2` Login | Entra na conta (senha + código enviado por e-mail) |
| `3` Perfil | Mostra os dados da conta |
| `4` Atualizar dados | Troca nome, troca senha ou deleta a conta |
| `5` Conversas | Abre o bate-papo |
| `6` Feed | Abre as postagens e enquetes |
| `7` Sair | Encerra o programa |

Dentro do **Feed**: `N` cria uma postagem, `O` troca a ordem, o número abre uma postagem, `+`/`-` curte ou descurte, `C` comenta e `E` vota na enquete.

Dentro das **Conversas**: `N` inicia uma conversa nova, o número abre uma conversa existente e, dentro dela, `Enter` atualiza as mensagens e `/sair` volta.
