import socket
import threading
import tkinter as tk
from tkinter import messagebox
from crypto_utils import generate_aes_key, encrypt, decrypt


class TicTacToeClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Aguardando oponente")
        self.buttons = []
        self.board = [" " for _ in range(9)]
        self.create_interface()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('localhost', 3000))
            print("Conectado ao servidor.")
        except ConnectionRefusedError:
            print("Falha na conexão. Certifique-se de que o servidor está em execução.")
            self.master.quit()
        threading.Thread(target=self.receive_data).start()

    def create_interface(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.master, text=" ", font='normal 20', width=5, height=2,
                                   command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def make_move(self, i, j):
        move = i * 3 + j
        if self.board[move] == " " and self.symbol:
            self.client_socket.send(str(move).encode())
            print(f"Enviando movimento: {move}")
        elif self.board[move] != " ":
            messagebox.showwarning("Movimento inválido",
                                   "Essa posição já está ocupada!")

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                print(f"Dados recebidos do servidor: {data}")
                if data.startswith("YOUR_TURN"):
                    self.master.title("Sua vez")
                    self.symbol = data.split()[-1]
                elif data.startswith("OPPONENT_TURN"):
                    self.master.title("Vez do oponente")
                elif data.startswith("YOU_WIN"):
                    messagebox.showinfo("Fim de Jogo", "Você venceu!")
                    self.master.quit()
                elif data.startswith("YOU_LOSE"):
                    messagebox.showinfo("Fim de Jogo", "Você perdeu!")
                    self.master.quit()
                elif data.startswith("DRAW"):
                    messagebox.showinfo("Fim de Jogo", "Empate!")
                    self.master.quit()
                elif data.startswith("INVALID_MOVE"):
                    messagebox.showwarning(
                        "Movimento inválido", "Tente novamente!")
                else:
                    self.update_interface(data)
            except socket.error as e:
                print(f"Erro de socket: {e}")
                break

    def update_interface(self, board_state):
        self.board = list(board_state)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i*3+j])
                self.buttons[i][j].update()


def main():
    root = tk.Tk()
    app = TicTacToeClient(root)
    root.mainloop()


if __name__ == "__main__":
    main()
