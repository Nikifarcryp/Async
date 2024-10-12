import socket
import selectors

selector = selectors.DefaultSelector()

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5555))
    server.listen()

    selector.register(fileobj=server, events=selectors.EVENT_READ, data=accept_connection)

def accept_connection(server):
    client, addr = server.accept()
    print('Connected with', addr)
    selector.register(fileobj=client, events=selectors.EVENT_READ, data=send_message)

def send_message(client):
    request = client.recv(4096)

    if not request:
        selector.unregister(client)
        client.close()
    else:
        response = 'Hello!'.encode('utf-8')
        client.send(response)

def event_loop():
    while True:
        events = selector.select()   # (key, event)
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)

if __name__ == '__main__':
    server()
    event_loop()
