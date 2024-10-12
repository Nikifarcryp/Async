import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9999))
server_socket.listen()
client_socket, addr = server_socket.accept()

done = False

while not done:
    msg = client_socket.recv(4096).decode('utf-8')
    if msg == 'quit':
        done = True
    else:
        print(msg)
    client_socket.send(input('Message: ').encode('utf-8'))

server_socket.close()
client_socket.close()