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
    # data es un objeto bytes que codifica los carácteres del string según utf-8
    data = txt.encode('utf-8')
    if len(data) > MAX_LEN:
        # review
        raise ValueError(f'Campo supera {MAX_LEN} bytes: {txt!r}')
    # crea un objeto bytes con los bytes de ambos
    sock.sendall(data + b'\0')

def recv_str(sock: socket.socket) -> str:
    # como el objeto bytes, pero un bytearray es mutable
    buf = bytearray()
    while True:
        # b es un objeto bytes que contiene un único byte
        b = sock.recv(1)
        if not b:
            # review
            raise ConnectionError('Conexión cerrada inesperadamente')
        # b'\0' es un objeto bytes que contiene el byte \0
        if b == b'\0':
            break
        buf.extend(b)
        if len(buf) > MAX_LEN:
            raise ValueError('Recibido demasiado largo')
    # una vez estamos seguros de tener todo el string, lo decodificamos y devolvemos
    return buf.decode('utf-8')

def recv_byte(sock: socket.socket) -> int:
    b = sock.recv(1)
    if not b:
        raise ConnectionError('No se recibió el código de resultado')
    # acceder a un elemento del objeto bytes devuelve el valor entero de ese byte
    return b[0]