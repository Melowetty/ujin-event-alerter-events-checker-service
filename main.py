import json
import socket
import threading
import requests

HOST = '46.146.226.121'  # IP-адрес сервера
PORT = 8070  # Порт сервера
POST_PATH = "internal/event"
INTERNAL_HOST = "localhost"
INTERNAL_PORT = 8080


def checkEvents(eventType: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    request = f"GET /event?login=root&password=&responsetype=json&filter={eventType} HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
    s.sendall(request.encode())
    data = s.recv(1024)
    while True:
        data = s.recv(2048)
        body = json.loads(data.decode("utf-8")[3:].strip())
        comment = body["Comment"]
        if comment == "KeepAlive":
            continue
        print(body)
        requests.post(f"http://{INTERNAL_HOST}:{INTERNAL_PORT}/{POST_PATH}", json=body).close()
        if not data:
            break


if __name__ == "__main__":
    threads = [
        threading.Thread(target=checkEvents, args=("65afbe3d-41b2-41d2-802a-dbd2a00db0ed",)),
        threading.Thread(target=checkEvents, args=("d99a411f-d0a6-42c4-b320-3c2dd0aa0821",)),
        threading.Thread(target=checkEvents, args=("bcad095a-f2b0-4c20-a7f0-88ee5da703b1",)),
    ]
    for thread in threads:
        thread.start()
