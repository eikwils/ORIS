import socket
import threading

from protocol import recv_message, send_message

clients = {}
clients_lock = threading.Lock()

def handle_client(conn):
    try:
        while True:
            message = recv_message(conn)

            if message is None:
                break

            command, payload = message

            if command == "JOIN":
                username = payload.decode()

                with clients_lock:
                    clients[conn] = username

            elif command == "TEXT":
                with clients_lock:
                    username = clients[conn]
                    client_list = list(clients)

                text = payload.decode()
                message_to_send = f"{username}: {text}"

                for client in client_list:
                    if client != conn:
                        try:
                            send_message(client, "TEXT", message_to_send.encode())
                        except (BrokenPipeError, ConnectionResetError):
                            pass

            elif command == "LIST":
                with clients_lock:
                    usernames = ", ".join(clients.values())

                send_message(conn, "LIST", usernames.encode())

            elif command == "QUIT":
                break

            else:
                send_message(conn, "ERRO", b"Unknown command")

    except ConnectionResetError:
        print("Клиент аварийно отключился")

    except BrokenPipeError:
        print("Соединение с клиентом потеряно")   

    finally:
        with clients_lock:
            username = clients.pop(conn, None)
            client_list = list(clients)

        conn.close()

        if username is not None:
            message = f"{username} вышел из чата"

            for client in client_list:
                try:
                    send_message(client, "TEXT", message.encode())
                except (BrokenPipeError, ConnectionResetError):
                    pass


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 10000))
s.listen()

print("Сервер запущен")

while True:
    conn, addr = s.accept()

    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()