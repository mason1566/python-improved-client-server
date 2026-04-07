class Request:
    def __init__(self, request_type, request_path, host, content_type = "", content = ""):
        self.request_type = request_type
        self.request_path = request_path
        self.host = host
        self.content_type = ""
        self.content_length = 0
        self.content = ""

    def request(self):
        request = ""
        if self.content:
            request = (
                f"{self.request_type} {self.request_path} HTTP/1.1\r\n"
                f"Host: {self.host}\r\n"
                f"Connection: close\r\n"
                f"Content-Type: {self.content_type or "text/html"}\r\n"
                f"Content-Length: {len(self.content)}\r\n"
                f"\r\n"
                f"{self.content}\r\n"
            )
        else:
            request = (
                f"{self.request_type} {self.request_path} HTTP/1.1\r\n"
                f"Host: {self.host}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )
        return request

# Assumes request lines end with "\r\n".
def getHeaderValue(requestHeader, header):
    value = requestHeader.partition(f"{header}: ")[2]
    value = value.partition("\r\n")[0]
    return value


def parseRequestHeader(requestHeader):
    headers = {}
    lines = requestHeader.split("\r\n")

    request_line = lines[0].split(" ")
    request_type = request_line[0]
    request_path = request_line[1]

    del lines[0]

    for header in lines:
        h = header.partition(": ")
        if h[1] == ": ":
            headers[f"{h[0]}"] = h[2]
    
    host = headers.get("Host", "")

    request = Request(request_type, request_path, host)

    request.content_type = headers.get("Content-Type", "")
    request.content_length = headers.get("Content-Length", "")

    return request


def generateResponse(status_code, status_message, content_type = "", content: str = ""):
    content_length = len(content)
    
    response = ""
    if content_length > 0:
        response = (
            f"HTTP/1.1 {status_code} {status_message}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {content_length}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"{content}"
        )
    else:
        response = (
            f"HTTP/1.1 {status_code} {status_message}\r\n"
            f"Content-Length: 0\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
    return response