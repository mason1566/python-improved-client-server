import socket
import argparse
from network_util import Request

parser = argparse.ArgumentParser()
parser.add_argument("host", nargs="?", default="example.com")
parser.add_argument("port", nargs="?", type=int, default=80)
parser.add_argument("request_type", nargs="?", default="GET")
parser.add_argument("content", nargs="*", default="Hello!")

args = parser.parse_args()

HOST = args.host
PORT = args.port
REQUEST_TYPE = args.request_type
REQUEST_CONTENT = " ".join(args.content) if type(args.content) is list else args.content

request = Request(REQUEST_TYPE, "/", f"{HOST}:{PORT}")

print(HOST, PORT)

sock = socket.socket()
sock.connect((HOST, PORT))

print("Connected!")

if REQUEST_CONTENT:
    request.content_type = "text/plain"
    request.content = REQUEST_CONTENT
    sock.sendall(request.request().encode('utf-8'))
else:
    sock.sendall(request.request().encode('utf-8'))

print("Sent request!")

buf = b""

while True:
    d = sock.recv(4096)
    if not d:
        break
    buf += d

buf = buf.decode("utf-8", errors="replace").replace("\\n", "\n") if len(buf) > 0 else ""
print(buf)