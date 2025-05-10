import socket

MAX_LEN = 256  # tamaño máximo de nombre, ruta, etc.

REGISTER_CODES = {
    0: "REGISTER OK",
    1: "USERNAME IN USE",
    2: "REGISTER FAIL",
}
REGISTER_DEFAULT_ERROR_VALUE = REGISTER_CODES.get(2)

UNREGISTER_CODES = {
    0: "UNREGISTER OK",
    1: "USER DOES NOT EXIST",
    2: "UNREGISTER FAIL"
}
UNREGISTER_DEFAULT_ERROR_VALUE = UNREGISTER_CODES.get(2)

def send_str(sock: socket.socket, txt: str) -> None:
    # data es un objeto bytes que codifica los carácteres del string según utf-8
    data = txt.encode('utf-8')
    # review: no enviar string si está vacío?
    if len(data) == 0:
        raise ValueError("El campo está vacío")
    elif len(data) > MAX_LEN:
        raise ValueError(f'El campo supera {MAX_LEN} bytes: {txt!r}')
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

def communicate_with_server(server: str, port: int, list_str: list, default_error_value: int) -> int:
    try:
        # with asegura cerrar el socket después de salir de él
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # timeout de 5 segundos para que si hay un fallo en las operaciones bloqueantes, el programa no quede bloqueado indefinidamente
            sock.settimeout(5)
            sock.connect((server, port))
            # envíamos todas las cadenas necesarias al servidor
            for string in list_str:
                send_str(sock, string)
            # devolvemos el código recibido
            return recv_byte(sock)
            
    # si hay cualquier tipo de error en el cliente, se devuelve el valor predeterminado de error
    except (socket.error, ValueError, ConnectionError, OSError, TimeoutError, UnicodeError) as e:
        return default_error_value


