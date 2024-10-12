import socket
from select import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 5555))
server.listen()

to_monitor = []
connected_devices = []
def accept_connection(server):
    client, addr = server.accept()
    connected_devices.append(addr)
    print('Connected devices: ', len(connected_devices))
    to_monitor.append(client)

def send_message(client):
    request = client.recv(4096)

    if not request:
        client.close()

    else:
        response = 'Hello!'.encode('utf-8')
        client.send(response)

def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server:
                accept_connection(sock)
            else:
                send_message(sock)

if __name__ == '__main__':
    to_monitor.append(server)
    event_loop()