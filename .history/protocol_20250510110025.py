import socket

MAX_LEN = 256  # tamaño máximo de nombre, ruta, etc.

def send_str(sock: socket.socket, txt: str) -> None:
    data = txt.encode('utf-8') + b'\0'
    sock.sendall(data)

def recv_str(sock: socket.socket) -> str:
    buf = bytearray()
    while True:
        b = sock.recv(1)
        if not b:
            raise ConnectionError('Conexión cerrada inesperadamente')
        if b == b'\0':
            break
        buf.extend(b)
        if len(buf) > MAX_LEN:
            raise ValueError('Recibido demasiado largo')
    return buf.decode('utf-8')

def recv_byte(sock: socket.socket) -> int:
    b = sock.recv(1)
    if not b:
        raise ConnectionError('No se recibió el código de resultado')
    return b[0]