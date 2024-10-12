import socket
from select import select

to_read = {}
to_write = {}
tasks = []


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 4444))
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        _client, addr = server_socket.accept()  # read
        print('Connected with:', addr)
        tasks.append(client(_client))

def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096).decode('utf-8')   # read

        if not request:
            break
        else:
            response = 'Hello World'.encode('utf-8')
            yield ('write', client_socket)
            client_socket.send(response)   # write

    client_socket.close()

def event_loop():
    while any([to_read, to_write, tasks]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except Exception:
            print('Done!')

tasks.append(server())
event_loop()