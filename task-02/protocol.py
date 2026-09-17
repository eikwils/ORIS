import struct
MAX_MESSAGE_SIZE = 10 * 1024 * 1024

def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if chunk == b"":
            raise ConnectionError("Соединение закрылось раньше времени")

        data += chunk

    return data


def send_message(sock, command, payload):
    command_bytes = command.encode()

    if len(command_bytes) != 4:
        raise ValueError("Команда должна занимать ровно 4 байта")
    
    length = len(payload)

    if length > MAX_MESSAGE_SIZE:
        raise ValueError("Сообщение слишком большое")

    length_bytes = struct.pack("!I", length)
    message = command_bytes + length_bytes + payload

    sock.sendall(message)


def recv_message(sock):
    command_bytes = sock.recv(4)

    if command_bytes == b"":
        return None

    if len(command_bytes) < 4:
        command_bytes += recv_exact(sock, 4 - len(command_bytes))

    command = command_bytes.decode()

    length_bytes = recv_exact(sock, 4)
    length = struct.unpack("!I", length_bytes)[0]

    if length > MAX_MESSAGE_SIZE:
        raise ValueError("Сообщение слишком большое")
    
    payload = recv_exact(sock, length)
    return command, payload