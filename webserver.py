import socket
import argparse
from network_util import Request, parse_http_request, generate_response #, GetRequest, PostRequest, DeleteRequest

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("port", nargs="?", type=int, default=28333)
parser.add_argument("host", nargs="?", default="")

args = parser.parse_args()

HOST = args.host
PORT = args.port

# Socket connection
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen()

# Server loop
while True:
    new_conn = sock.accept()
    new_sock = new_conn[0]

    buf = b''

    while True:
        d = new_sock.recv(4096)
        buf += d
        if b"\r\n\r\n" in buf:
            break
        
    buf = buf.decode("utf-8", errors="replace").replace("\\n", "\n").replace("\\r", "\r") if len(buf) > 0 else ""

    request = parse_http_request(buf)

    print(request.request())

    response = generate_response("200", "OK")
    # print(response)
    
    new_sock.sendall(response.encode('utf-8'))
    new_sock.close()

    buf = b""
    print("Connection closed!\n")

