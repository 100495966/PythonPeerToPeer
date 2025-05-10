import socket

MAX_LEN = 256  # tamaño máximo de nombre, ruta, etc.

REGISTER_CODES = {
    0: "REGISTER OK",
    1: "USERNAME IN USE",
    2: "REGISTER FAIL"
}

def send_str(sock: socket.socket, txt: str) -> None:
    # data es un objeto bytes que codifica los carácteres del string según utf-8
    data = txt.encode('utf-8')
    if len(data) > MAX_LEN:
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

def register(server: str, port: int, user: str) -> str:
    try:
        # with asegura cerrar el socket después de salir de él
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # timeout de 5 segundos para que si hay un fallo en las operaciones bloqueantes, el programa no quede bloqueado indefinidamente
            sock.settimeout(5)
            sock.connect((server, port))
            send_str(sock, "REGISTER")
            send_str(sock, user)
            code = recv_byte(sock)
            msg  = REGISTER_CODES.get(code, f'REGISTER FAIL')
            return msg
    except (socket.error, ValueError, ConnectionError) as e:
        return "REGISTER FAIL"

