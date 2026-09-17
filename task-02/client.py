import socket
import threading

from protocol import send_message, recv_message


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 10000))

username = input("Введите имя: ")
send_message(s, "JOIN", username.encode())


def receive_messages():
    try:
        while True:
            message = recv_message(s)

            if message is None:
                print("Сервер закрыл соединение")
                break

            command, payload = message
            text = payload.decode()

            if command == "TEXT":
                print(text)

            elif command == "LIST":
                print("Пользователи:", text)

            elif command == "ERRO":
                print("Ошибка:", text)

    except ConnectionResetError:
        print("Соединение с сервером потеряно")

    except OSError:
        print("Соединение закрыто")


def send_commands():
    while True:
        user_input = input()

        if user_input == "/list":
            send_message(s, "LIST", b"")

        elif user_input == "/quit":
            send_message(s, "QUIT", b"")
            break

        else:
            send_message(s, "TEXT", user_input.encode())


receiver = threading.Thread(target=receive_messages)
receiver.start()

send_commands()

s.close()