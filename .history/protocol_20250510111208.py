import socket

MAX_LEN = 256  # tamaño máximo de nombre, ruta, etc.

# review mapeo de códigos de resultado a texto
RESULT_CODES = {
    0: 'OK',
    1: 'USER DOES NOT EXIST',
    2: 'USER NOT CONNECTED',
    3: 'CONTENT NOT PUBLISHED',
    4: 'FAIL',
    # todo …otros códigos según cada operación…
}

def send_str(sock: socket.socket, txt: str) -> None:
    data = txt.encode('utf-8')
    if len(data) > MAX_LEN:
        // review: REGISTER FAIL?
        raise ValueError(f'Campo supera {MAX_LEN} bytes: {txt!r}')
    sock.sendall(data + b'\0')

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