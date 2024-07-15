
# Jogo da Velha com criptografia  em grupo

Este projeto implementa um jogo da velha multiplayer com interface gráfica para os jogadores e um servidor central que gerencia o jogo. O servidor aguarda a conexão de dois jogadores, distribui os símbolos (X e O), gerencia as jogadas, verifica a vitória ou empate e notifica os jogadores do resultado.


Índice
=================
* [Diretórios](#diretórios)
* [Arquitetura](#arquitetura)
     * [Servidor](#caso-1)
     * [Jogador 1](#Jogador-1)
     * [Jogador 2](#Jogador-2)
* [Instruções de uso](#instruções-de-uso)
* [Interface gráfica](#interface-gráfica)
* [Infraestrutura](#infraestrutura)
* [Considerações adicionais](#considerações-adicionais)

<br>

</br>

## Diretórios

```
trabalhoRedesGroupCrypto/
└── .gitignore
├── client.py
├── crypto_utils.py 
├── README.md
└── server.py   
```

Diretórios:

- `server.py`: Este arquivo contém o código do servidor do jogo da velha. Ele é responsável por iniciar o servidor, gerenciar as conexões dos jogadores, controlar o fluxo do jogo e enviar mensagens para os jogadores.
- `client.py`: Este arquivo contém o código do cliente do jogo da velha. Ele é responsável por conectar-se ao servidor, receber mensagens do servidor, atualizar a interface gráfica e enviar jogadas para o servidor.
- `crypto_utils.py`: Este arquivo contém funções para criptografar e descriptografar mensagens usando o algoritmo AES. Isso é usado para proteger a comunicação entre o servidor e os jogadores.




## Arquitetura

A aplicação é dividida em três partes principais:

### Servidor

- **Arquivo:** `server.py`
- **Funcionalidade:**
  - Inicia o servidor e aguarda conexões de jogadores na porta 3000.
  - Recebe as conexões dos jogadores e as armazena em uma lista.
  - Quando dois jogadores estão conectados, inicia o jogo:
    - Sorteia aleatoriamente qual jogador começa.
    - Envia o estado do tabuleiro e a vez de jogar para cada jogador.
    - Recebe as jogadas dos jogadores, atualiza o estado do tabuleiro e verifica se há um vencedor ou empate.
    - Envia o resultado do jogo para os jogadores e fecha as conexões.

### Jogador 1

- **Arquivo:** `client.py`
- **Funcionalidade:**
  - Conecta-se ao servidor na porta 3000.
  - Recebe as mensagens do servidor e atualiza a interface gráfica de acordo com o estado do jogo.
  - Envia as jogadas do jogador para o servidor.

### Jogador 2

- **Arquivo:** `client.py` (mesmo arquivo do Jogador 1)
- **Funcionalidade:**
  - Conecta-se ao servidor na porta 3000.
  - Recebe as mensagens do servidor e atualiza a interface gráfica de acordo com o estado do jogo.
  - Envia as jogadas do jogador para o servidor.

## Instruções de uso

### Servidor

Execute o seguinte comando em um terminal:

```
python server.py
```

O servidor estará em execução na porta 3000.

### Jogador 1

Abra um novo terminal e execute o seguinte comando:

```
python client.py
```

O jogador 1 estará conectado ao servidor e aguardando outro jogador.

### Jogador 2

Abra outro novo terminal e execute o seguinte comando:

```
python client.py
```

O jogador 2 estará conectado ao servidor e o jogo começará.

## Interface gráfica

A interface gráfica do jogo da velha é simples e intuitiva. Ela exibe o tabuleiro do jogo com as jogadas dos jogadores e indica a vez de quem joga. O jogador pode clicar em qualquer quadrado vazio do tabuleiro para fazer sua jogada. A interface gráfica também exibe mensagens do servidor, como o resultado do jogo.


## Infraestrutura

A infraestrutura do jogo da velha é composta por três componentes principais:

1. **Servidor:** O servidor é o componente central do jogo. Ele é responsável por gerenciar o jogo e a comunicação com os jogadores.
2. **Jogadores:** Os jogadores são os clientes que se conectam ao servidor para jogar o jogo.
3. **Rede:** A rede é a infraestrutura que conecta o servidor e os jogadores. Ela pode ser uma rede local ou uma rede de internet.

## Considerações adicionais

- O jogo da velha foi implementado em Python com a biblioteca Tkinter para criar a interface gráfica.
- A criptografia AES foi usada para proteger a comunicação entre o servidor e os jogadores.