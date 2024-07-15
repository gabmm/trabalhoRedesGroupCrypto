import socket
import threading
import random
from crypto_utils import generate_aes_key, encrypt, decrypt


def check_winner(position):
    winning_combinations = [
        [position[0], position[1], position[2]],
        [position[3], position[4], position[5]],
        [position[6], position[7], position[8]],
        [position[0], position[3], position[6]],
        [position[1], position[4], position[7]],
        [position[2], position[5], position[8]],
        [position[0], position[4], position[8]],
        [position[2], position[4], position[6]]
    ]
    for combination in winning_combinations:
        if ((combination[0] == combination[1] == combination[2]) and combination[0] != " "):
            return True
    return False


def check_draw(position):
    return " " not in position


def send_position(conn1, conn2, position):
    position_state = "".join(position)
    try:
        conn1.send(position_state.encode())
        conn2.send(position_state.encode())
    except socket.error as e:
        print(f"Erro ao enviar o tabuleiro: {e}")


def game_manager(conn1, conn2, all_connections):
    positions = [" " for _ in range(9)]
    players = [conn1, conn2]
    symbols = ["X", "O"]
    current_player = random.choice([0, 1])

    send_position(conn1, conn2, positions)
    print("Tabuleiro inicial enviado aos jogadores.")

    while True:
        player = players[current_player]
        symbol = symbols[current_player]

        try:
            player.send(f"YOUR_TURN {symbol}".encode())
            players[1 - current_player].send("OPPONENT_TURN".encode())
            move = player.recv(1024).decode()
            print(f"Jogador {current_player +
                  1} ({symbol}) escolheu posição {move}.")
        except socket.error as e:
            print(f"Erro de socket: {e}")
            break

        try:
            move = int(move)
            if move < 0 or move >= len(positions):
                player.send("INVALID_MOVE".encode())
                print("Movimento inválido: índice fora do intervalo.")
                continue
        except ValueError:
            player.send("INVALID_MOVE".encode())
            print("Movimento inválido: não é um número.")
            continue

        if positions[move] == " ":
            positions[move] = symbol
            send_position(conn1, conn2, positions)
            print(f"Tabuleiro atualizado: {positions}")
            if check_winner(positions):
                player.send("YOU_WIN".encode())
                players[1 - current_player].send("YOU_LOSE".encode())
                print(f"Jogador {current_player + 1} ({symbol}) venceu.")
                break
            elif check_draw(positions):
                conn1.send("DRAW".encode())
                conn2.send("DRAW".encode())
                print("Empate.")
                break
            current_player = 1 - current_player
        else:
            player.send("INVALID_MOVE".encode())
            print("Movimento inválido: posição já ocupada.")

    conn1.close()
    conn2.close()
    all_connections.clear()


def handle_client(conn, addr, all_connections):
    print(f"Jogador {addr} conectado.")
    all_connections.append(conn)
    if len(all_connections) == 2:
        print("Servidor inicializado! \nAguardando jogadores...")
        threading.Thread(target=game_manager, args=(
            all_connections[0], all_connections[1], all_connections)).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 3000))
    server.listen(2)
    print("Servidor aguardando conexões...")

    all_connections = []

    while True:
        conn, addr = server.accept()
        print(f"Conexão aceita de {addr}")
        threading.Thread(target=handle_client, args=(
            conn, addr, all_connections)).start()


if __name__ == "__main__":
    main()
