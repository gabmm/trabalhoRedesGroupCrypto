import socket
import pickle
import threading
import random
from crypto_utils import encrypt, decrypt, generate_random_iv, generate_random_key


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


def send_position(conn1, conn2, position, all_Keys):
    key = all_Keys[0]
    iv = all_Keys[1]
    position_state = "".join(position)
    mensage = position_state.encode()
    encrypted_message = encrypt(mensage, key, iv)
    try:
        conn1.send(encrypted_message)
        conn2.send(encrypted_message)
        # print(encrypted_message)
    except socket.error as e:
        print(f"Erro ao enviar o tabuleiro: {e}")


def game_manager(conn1, conn2, all_connections, all_Keys):
    positions = [" " for _ in range(9)]
    players = [conn1, conn2]
    symbols = ["X", "O"]
    key = all_Keys[0]
    iv = all_Keys[1]
    current_player = random.choice([0, 1])

    send_position(conn1, conn2, positions, all_Keys)
    print("Tabuleiro inicial enviado aos jogadores.")
    print(f"Tabuleiro atualizado: {positions}")
    while True:
        player = players[current_player]
        symbol = symbols[current_player]

        try:
            message = f"YOUR_TURN Your symbol: {symbol}".encode()
            encrypted_message = encrypt(message, key, iv)
            player.send(encrypted_message)

            message = f"OPPONENT_TURN Your symbol: {
                symbols[1 - current_player]}".encode()
            encrypted_message = encrypt(message, key, iv)
            players[1 - current_player].send(encrypted_message)

            move = player.recv(1024)

            print(f"(criptografada): Jogador {current_player +
                  1} ({symbol}) escolheu posição {move}.")

            move = decrypt(move, key, iv).decode()

            print(f"(descriptografada): Jogador {current_player +
                  1} ({symbol}) escolheu posição {move}.")
        except socket.error as e:
            print(f"Erro de socket: {e}")
            break

        try:
            move = int(move)
            if move < 0 or move >= len(positions):

                player.send(encrypt("INVALID_MOVE".encode(), key, iv))
                print("Movimento inválido: índice fora do intervalo.")
                continue
        except ValueError:
            player.send(encrypt("INVALID_MOVE".encode(), key, iv))
            print("Movimento inválido: não é um número.")
            continue

        if positions[move] == " ":
            positions[move] = symbol
            send_position(conn1, conn2, positions, all_Keys)
            print(f"Tabuleiro atualizado: {positions}")
            if check_winner(positions):
                player.send(encrypt("YOU_WIN".encode(), key, iv))
                players[1 -
                        current_player].send(encrypt("YOU_LOSE".encode(), key, iv))
                print(f"Jogador {current_player + 1} ({symbol}) venceu.")
                break
            elif check_draw(positions):
                conn1.send(encrypt("DRAW".encode(), key, iv))
                conn2.send(encrypt("DRAW".encode(), key, iv))
                print("Empate.")
                break
            current_player = 1 - current_player
        else:
            player.send(encrypt("INVALID_MOVE".encode(), key, iv))
            print("Movimento inválido: posição já ocupada.")

    conn1.close()
    conn2.close()
    all_connections.clear()


def handle_client(conn, addr, all_connections):
    print(f"Jogador {addr} conectado.")
    all_connections.append(conn)
    if len(all_connections) == 2:
        print("Servidor inicializado! \nAguardando jogadores...")
        key = generate_random_key()
        iv = generate_random_iv()
        all_Keys = [key, iv]
        serialized_keys = pickle.dumps(all_Keys)
        all_connections[0].send(serialized_keys)
        all_connections[1].send(serialized_keys)
        print(key)
        print(iv)
        print("Enviado as chaves para criptografia aos jogadores!")

        threading.Thread(target=game_manager, args=(
            all_connections[0], all_connections[1], all_connections, all_Keys)).start()


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
